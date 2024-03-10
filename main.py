import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from utils.commands import set_commands

from user.user_handler import (start_handler, name_get_handler, hair_coloring_get_handler,
                               hair_photo_get_handler, phone_number_get_handler,
                               free_dates_get_handler, free_times_get_handler)
from user.user_callback import (order_main_menu_callback, hair_length_get_callback,
                                additional_services_get_callback, hair_density_get_callback,
                                first_time_get_callback, hair_coloring_get_callback, service_get_callback,
                                hair_photo_get_callback)
from user.user_utils import User

router = Router()


async def start_bot(bot: Bot):
    load_dotenv()
    await set_commands(bot)
    await bot.send_message(os.getenv("ADMIN_ID"), text='Бот запущен!')


async def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(os.getenv("TOKEN"), parse_mode="HTML")

    dp.startup.register(start_bot)

    dp.message.register(start_handler, Command('start'))

    dp.callback_query.register(order_main_menu_callback, F.data.startswith('order_main_menu'))

    dp.callback_query.register(hair_density_get_callback, F.data.startswith('hair_density_0'))
    dp.callback_query.register(hair_density_get_callback, F.data.startswith('hair_density_500'))
    dp.callback_query.register(hair_density_get_callback, F.data.startswith('hair_density_1000'))

    dp.callback_query.register(hair_length_get_callback, F.data.startswith('hair_length_3000'))
    dp.callback_query.register(hair_length_get_callback, F.data.startswith('hair_length_3500'))
    dp.callback_query.register(hair_length_get_callback, F.data.startswith('hair_length_4000'))
    dp.callback_query.register(hair_length_get_callback, F.data.startswith('hair_length_4500'))
    dp.callback_query.register(hair_length_get_callback, F.data.startswith('hair_length_5000'))
    dp.callback_query.register(hair_length_get_callback, F.data.startswith('hair_length_8000'))

    dp.callback_query.register(additional_services_get_callback, F.data.startswith('cold_regen_1500_✅'))
    dp.callback_query.register(additional_services_get_callback, F.data.startswith('polishing_1000_✅'))
    dp.callback_query.register(additional_services_get_callback, F.data.startswith('smooth_cut_500_✅'))
    dp.callback_query.register(additional_services_get_callback, F.data.startswith('cold_regen_1500_❌'))
    dp.callback_query.register(additional_services_get_callback, F.data.startswith('polishing_1000_❌'))
    dp.callback_query.register(additional_services_get_callback, F.data.startswith('smooth_cut_500_❌'))
    dp.callback_query.register(additional_services_get_callback, F.data.startswith('additional_services_continue'))
    dp.callback_query.register(first_time_get_callback, F.data.startswith('first_time_yes'))
    dp.callback_query.register(first_time_get_callback, F.data.startswith('first_time_no'))
    dp.callback_query.register(hair_coloring_get_callback, F.data.startswith('hair_coloring_no'))
    dp.callback_query.register(hair_photo_get_callback, F.data.startswith('unsend_hair_photo'))

    dp.callback_query.register(service_get_callback, F.data.startswith('ceratin'))
    dp.callback_query.register(service_get_callback, F.data.startswith('botoks'))
    dp.callback_query.register(service_get_callback, F.data.startswith('biskiplastiya'))

    dp.message.register(name_get_handler, User.name_get)
    dp.message.register(hair_coloring_get_handler, User.hair_coloring)
    dp.message.register(hair_photo_get_handler, User.hair_photo)
    dp.message.register(phone_number_get_handler, User.phone_number)
    dp.message.register(free_dates_get_handler, User.free_dates)
    dp.message.register(free_times_get_handler, User.free_times)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
