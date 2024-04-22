from aiogram import Router, F, types

from app.utils.aggregation_salary import aggregation_salary

import ast


router = Router()


@router.message()
async def aggregation_handler(message: types.Message):

    data = ast.literal_eval(message.text.replace("\n", ""))
    output_data = await aggregation_salary(data=data)
    await message.answer(str(output_data))
