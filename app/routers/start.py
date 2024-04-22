from aiogram import Router, types
from aiogram.filters.command import CommandStart


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):

    user_info = message.from_user

    await message.answer(
        text=f"Hi <a href='https://t.me/{user_info.username}'>{user_info.first_name}</a>"
    )
