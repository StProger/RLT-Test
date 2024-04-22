from aiogram import Dispatcher

from . import start
from .user import aggregation


def register_all_routers(dp: Dispatcher):

    dp.include_router(start.router)
    dp.include_router(aggregation.router)
