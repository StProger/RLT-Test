from aiogram import Router, F, types

from app.utils.aggregation_salary import aggregation_salary
from app.settings import settings

import ast


router = Router()


@router.message()
async def aggregation_handler(message: types.Message):

    text = """Невалидный запрос. Пример запроса:
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}"""
    try:
        data = ast.literal_eval(message.text.replace("\n", ""))
    except ValueError:
        await message.answer(text)
        return
    if data not in settings.valid_data:
        await message.answer(text)
    else:
        output_data = await aggregation_salary(data=data)
        await message.answer(str(output_data))
