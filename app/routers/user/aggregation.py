from aiogram import Router, F, types

from app.utils.aggregation_salary import aggregation_salary
from app.settings import settings

import ast


router = Router()


@router.message()
async def aggregation_handler(message: types.Message):


    try:

        data = ast.literal_eval(message.text.replace("\n", ""))

    except ValueError:

        text = """Невалидный запрос. Пример запроса:
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}"""

        await message.answer(text)
        return

    if data not in settings.valid_data:

        text = """Допустимо отправлять только следующие запросы:
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}
{"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"}
{"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}"""

        await message.answer(text)
    else:
        output_data = await aggregation_salary(data=data)
        await message.answer(str(output_data).replace("'", "\""))
