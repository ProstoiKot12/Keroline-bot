import math
from datetime import datetime
import os
import re

from aiogram import Bot
from dotenv import load_dotenv

from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from user.user_keyboards import main_menu_kb, hair_length_kb, specify_phone_kb, service_kb, unsend_hair_photo_kb
from user.user_utils import User
from google_request import get_free_slot, get_free_slots, insert_new


async def start_handler(message: Message):
    await message.answer('<b>Главное меню</b>', reply_markup=main_menu_kb)


async def name_get_handler(message: Message, state: FSMContext):
    name_pattern = re.compile(r'^\w+\s\w+$')

    if name_pattern.match(message.text):
        await state.update_data(name=message.text)
        await message.answer('Выберите услугу', reply_markup=service_kb)

    else:
        await message.answer('Введите <b>Имя и Фамилию</b>')


async def hair_coloring_get_handler(message: Message, state: FSMContext):
    await state.update_data(hair_coloring=message.text)

    await message.answer('Пришлите, пожалуйста, фото волос со спины', reply_markup=unsend_hair_photo_kb)
    await state.set_state(User.hair_photo)


async def hair_photo_get_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(hair_photo=message.photo)

        await message.answer('Укажите номер телефона', reply_markup=specify_phone_kb)
        await state.set_state(User.phone_number)
    else:
        await message.answer('Пришлите, пожалуйста, фото волос со спины', reply_markup=unsend_hair_photo_kb)


async def phone_number_get_handler(message: Message, state: FSMContext, bot: Bot):
    check = False
    try:
        await state.update_data(phone_number=message.contact.phone_number)
        check = True
    except Exception as a:
        await message.answer('Укажите номер телефона', reply_markup=specify_phone_kb)

    if check is True:

        result = await get_free_slot()

        dates = ''

        for date in result:
            dates += f"<code>{date}</code> \n"

        await message.answer('Введите желаемую дату\n'
                                  'Нажав на дату можно ее скопировать\n\n'
                                  f'{dates}', reply_markup=ReplyKeyboardRemove())

        await state.set_state(User.free_dates)


async def free_dates_get_handler(message: Message, state: FSMContext, bot: Bot):
    result = await get_free_slot()

    check = False

    for row in result:
        if row == message.text.strip():
            check = True

    if check is True:
        slots = 'Свободное время: \n'
        free_slots = await get_free_slots(message.text.strip())

        for slot in free_slots:
            slots += f"<b>с {slot[0].strftime('%H:%M')} до {slot[1].strftime('%H:%M')}</b>\n"

        await state.update_data(date=message.text.strip())

        await message.answer('Введите удобное вам время в формате ЧЧ:ММ\n\n'
                             f'{slots}')

        await state.set_state(User.free_times)
    else:
        dates = ''

        for date in result:
            dates += f"<code>{date}</code> \n"

        await message.answer('Введите желаемую дату\n\n'
                                f'{dates}')


async def free_times_get_handler(message: Message, state: FSMContext, bot: Bot):
    time_format_regex = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'

    if re.match(time_format_regex, message.text.strip()):

        data = await state.get_data()
        name = data['name']
        hair_length_price = data['hair_length_price']
        hair_length_name = data['hair_length_name']
        hair_density_price = data['hair_density_price']
        hair_density_name = data['hair_density_name']
        cold_regen = data['cold_regen']
        polishing = data['polishing']
        smooth_cut = data['smooth_cut']
        first_time = data['first_time']
        hair_coloring = data['hair_coloring']
        hair_photo = data['hair_photo']
        phone_number = data['phone_number']
        date = data['date']
        service = data['service']
        time = message.text.strip()

        price = int(hair_length_price) + int(hair_density_price) + int(cold_regen) + int(polishing) + int(smooth_cut)

        text = ('<b>Поздравляем, вы записаны на процедуру</b>\n\n'
                                 f'Услуга: <b>{service}</b>\n'
                                 f'Длина: <b>{hair_length_name}</b>\n'
                                 f'Густота: <b>{hair_density_name}</b>\n\n')
        services = 'Доп услуг нету'

        if polishing == 0 and smooth_cut == 0 and cold_regen != 0:
            text += (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>\n\n')

            services = (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>')
        elif cold_regen == 0 and polishing == 0 and smooth_cut != 0:
            text += (f'Доп услуги:\n'
                     f'<b>Ровный срез 500₽</b>\n\n')

            services = (f'Доп услуги:\n'
                     f'<b>Ровный срез 500₽</b>')
        elif smooth_cut == 0 and cold_regen == 0 and polishing != 0:
            text += (f'Доп услуги:\n'
                     f'<b>Полировка 1000₽</b>\n\n')

            services = (f'Доп услуги:\n'
                     f'<b>Полировка 1000₽</b>')
        elif smooth_cut != 0 and cold_regen != 0 and polishing != 0:
            text += (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>\n'
                     f'<b>Полировка 1000₽</b>\n'
                     f'<b>Ровный срез 500₽</b>\n\n')

            services = (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>\n'
                     f'<b>Полировка 1000₽</b>\n'
                     f'<b>Ровный срез 500₽</b>')
        elif cold_regen != 0 and polishing != 0 and smooth_cut == 0:
            text += (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>\n'
                     f'<b>Полировка 1000₽</b>\n\n')

            services = (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>\n'
                     f'<b>Полировка 1000₽</b>')
        elif cold_regen != 0 and polishing == 0 and smooth_cut != 0:
            text += (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>\n'
                     f'<b>Ровный срез 500₽</b>\n\n')

            services = (f'Доп услуги:\n'
                     f'<b>Холодное восстановление 1500₽</b>\n'
                     f'<b>Ровный срез 500₽</b>')
        elif cold_regen == 0 and polishing != 0 and smooth_cut != 0:
            text += (f'Доп услуги:\n'
                     f'<b>Полировка 1000₽</b>\n'
                     f'<b>Ровный срез 500₽</b>\n\n')

            services = (f'Доп услуги:\n'
                     f'<b>Полировка 1000₽</b>\n'
                     f'<b>Ровный срез 500₽</b>')

        text += (f'Дата: <b>{date}</b>\n'
                 f'Время: <b>{time}</b>\n\n'
                 f'К оплате: <b>{price}</b>\n\n'
                 'Благодарю Вас, в ближайшее время с Вами свяжусь для подтверждения записи✨')

        await message.answer(text)
        username = message.from_user.username
        if message.from_user.username is None:
            username = f"+{phone_number}"
        text = (f'<b>Новая заявка</b>\n\n'
                f'Имя: <b>{name}</b>\n'
                f"User name: <a href='https://t.me/{username}'>{username}</a>\n"
                f'Услуга: <b>{service}</b>\n'
                f'Длина: <b>{hair_length_name}</b>\n'
                f'Густота: <b>{hair_density_name}</b>\n'
                f'{services}\n'
                f"Впервый ли раз: <b>{first_time}</b>\n"
                f"Окрашивание волос: <b>{hair_coloring}</b>\n"
                f"Номер телефона: <code>{phone_number}</code>\n\n"
                f"К оплате: <b>{price}₽</b>")

        if hair_photo == 'Не захотел':
            await bot.send_message(chat_id=os.getenv('CHAT_ID'), text=text)
        else:
            photo = hair_photo[-1]
            await bot.send_photo(chat_id=os.getenv('CHAT_ID'), caption=text, photo=photo.file_id)

        date = datetime.strptime(date, "%Y-%m-%d").date()
        await insert_new(date, time, name, hair_length_name, hair_density_name, services, first_time, hair_coloring,
                         phone_number, service, price)

        await state.clear()

    else:
        data = await state.get_data()
        date = data['date']

        slots = 'Свободное время: \n'
        free_slots = await get_free_slots(date)

        for slot in free_slots:
            slots += f"<b>с {slot[0].strftime('%H:%M')} до {slot[1].strftime('%H:%M')}</b>\n"

        await message.answer('Введите удобное вам время в формате ЧЧ:ММ\n\n'
                             f'{slots}')



