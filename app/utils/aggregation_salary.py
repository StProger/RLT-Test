from pandas import DataFrame
import pandas as pd

from datetime import datetime, timedelta

from app.database.engine import get_database
from app.database.models import SalaryModel

from pymongo import ASCENDING


async def aggregation_salary(data):
    """ Вычисление агрегации """

    db = get_database()
    collection = db.sample_collection
    start_time = datetime.fromisoformat(data["dt_from"])
    end_time = datetime.fromisoformat(data["dt_upto"])

    data_collection = collection.find({"dt": {"$gte": start_time, "$lte": end_time}}).sort("dt", ASCENDING)

    items_df = DataFrame(data_collection)

    group_type = data["group_type"]
    output_data = {"dataset": [], "labels": []}

    if group_type == "hour":
        last_hour = None
        last_dt = None
        sum_salary = 0
        for item in items_df.itertuples():

            item: SalaryModel
            if last_hour is None:
                last_hour = item.dt.hour
                last_dt = item.dt
                sum_salary += item.value
            else:

                if last_hour == item.dt.hour:
                    sum_salary += item.value
                else:
                    label = pd.to_datetime(last_dt)
                    output_data["dataset"].append(sum_salary)
                    output_data["labels"].append((label.replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")))
                    sum_salary = item.value
                    last_hour = item.dt.hour
                    last_dt = item.dt
        label = pd.to_datetime(last_dt)
        output_data["dataset"].append(sum_salary)
        output_data["labels"].append(label.replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S"))
        if last_hour != 0:
            output_data["dataset"].append(0)
            output_data["labels"].append(data["dt_upto"])

    elif group_type == "month":

        last_month = None
        last_dt = None
        sum_salary = 0
        for item in items_df.itertuples():

            item: SalaryModel

            if last_month is None:
                last_month = item.dt.month
                last_dt = item.dt
                sum_salary += item.value
            else:

                if last_month == item.dt.month:
                    sum_salary += item.value
                else:
                    label = pd.to_datetime(last_dt)
                    output_data["dataset"].append(sum_salary)
                    output_data["labels"].append(
                        (label.replace(day=1, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")))
                    sum_salary = item.value
                    last_month = item.dt.month
                    last_dt = item.dt
        label = pd.to_datetime(last_dt)
        output_data["dataset"].append(sum_salary)
        output_data["labels"].append(
            label.replace(day=1, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S"))

    elif group_type == "day":

        last_day = None
        last_dt = None
        sum_salary = 0
        for item in items_df.itertuples():

            item: SalaryModel

            if last_day is None:
                last_day = item.dt.day
                last_dt = item.dt
                sum_salary += item.value

                # Заполняем нулями зп в начале месяца, если нет
                if last_day > 1:
                    for day in range(1, last_day):
                        output_data["dataset"].append(0)
                        output_data["labels"].insert(
                            0,
                            (last_dt - timedelta(days=day)).replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")
                        )
            else:

                if last_day == item.dt.day:
                    sum_salary += item.value
                else:
                    label = pd.to_datetime(last_dt)
                    output_data["dataset"].append(sum_salary)
                    output_data["labels"].append(
                        (label.replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")))
                    sum_salary = item.value
                    last_day = item.dt.day
                    last_dt = item.dt
        label = pd.to_datetime(last_dt)
        output_data["dataset"].append(sum_salary)
        output_data["labels"].append(
            label.replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S"))
    return output_data
