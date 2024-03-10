import math
from datetime import datetime
import os
import re

from aiogram import Bot
from dotenv import load_dotenv

from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from user.user_utils import User
from user.user_keyboards import (hair_density_kb, create_additional_services_kb,
                                 first_time_kb, hair_coloring_kb, hair_length_kb,
                                 specify_phone_kb, unsend_hair_photo_kb)


async def order_main_menu_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')

    await call.message.answer('Введите <b>Имя и Фамилию</b>')
    await state.set_state(User.name_get)


async def hair_length_get_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')

    hair_length_price = re.findall(r'\d+', call.data)[0]

    hair_length_name = ''
    if hair_length_price == '3000':
        hair_length_name = 'До плеч 3000₽'
    elif hair_length_price == '3500':
        hair_length_name = 'До лопаток 3500₽'
    elif hair_length_price == '4000':
        hair_length_name = 'Ниже лопаток 4000₽'
    elif hair_length_price == '4500':
        hair_length_name = 'До талии 4500₽'
    elif hair_length_price == '5000':
        hair_length_name = 'Ниже талии 5000₽'
    elif hair_length_price == '8000':
        hair_length_name = 'До колен 8000₽'

    await state.update_data(hair_length_price=hair_length_price)
    await state.update_data(hair_length_name=hair_length_name)

    await call.message.answer('Выберите <b>густоту волос</b>', reply_markup=hair_density_kb)


async def hair_density_get_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')

    hair_density_price = re.findall(r'\d+', call.data)[0]

    hair_density_name = ''
    if hair_density_price == '0':
        hair_density_name = 'Не густые 0₽'
    elif hair_density_price == '500':
        hair_density_name = 'Средняя густота 500₽'
    elif hair_density_price == '1000':
        hair_density_name = 'Очень густые 1000₽'

    await state.update_data(hair_density_price=hair_density_price)
    await state.update_data(hair_density_name=hair_density_name)

    additional_services_kb = await create_additional_services_kb("❌", "❌", "❌")

    await state.update_data(cold_regen=0)
    await state.update_data(polishing=0)
    await state.update_data(smooth_cut=0)

    await call.message.answer('Выберите дополнительные услуги', reply_markup=additional_services_kb)


async def additional_services_get_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')

    additional_services_kb = None

    if call.data == 'cold_regen_1500_❌':
        data = await state.get_data()
        await state.update_data(cold_regen=1500)
        if data['polishing'] == 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("✅", "❌", "❌")
        elif data['polishing'] != 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("✅", "✅", "❌")
        elif data['polishing'] == 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("✅", "❌", "✅")
        elif data['polishing'] != 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("✅", "✅", "✅")

        await call.message.edit_reply_markup(reply_markup=additional_services_kb,
                                             inline_message_id=call.inline_message_id)
    elif call.data == 'cold_regen_1500_✅':
        data = await state.get_data()
        await state.update_data(cold_regen=0)
        if data['polishing'] == 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("❌", "❌", "❌")
        elif data['polishing'] != 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("❌", "✅", "❌")
        elif data['polishing'] == 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("❌", "❌", "✅")
        elif data['polishing'] != 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("❌", "✅", "✅")

        await call.message.edit_reply_markup(reply_markup=additional_services_kb,
                                             inline_message_id=call.inline_message_id)

    if call.data == 'polishing_1000_❌':
        data = await state.get_data()
        await state.update_data(polishing=1000)
        if data['cold_regen'] == 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("❌", "✅", "❌")
        elif data['cold_regen'] != 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("✅", "✅", "❌")
        elif data['cold_regen'] == 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("❌", "✅", "✅")
        elif data['cold_regen'] != 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("✅", "✅", "✅")

        await call.message.edit_reply_markup(reply_markup=additional_services_kb,
                                             inline_message_id=call.inline_message_id)
    elif call.data == 'polishing_1000_✅':
        data = await state.get_data()
        await state.update_data(polishing=0)
        if data['cold_regen'] == 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("❌", "❌", "❌")
        elif data['cold_regen'] != 0 and data['smooth_cut'] == 0:
            additional_services_kb = await create_additional_services_kb("✅", "❌", "❌")
        elif data['cold_regen'] == 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("❌", "❌", "✅")
        elif data['cold_regen'] != 0 and data['smooth_cut'] != 0:
            additional_services_kb = await create_additional_services_kb("✅", "❌", "✅")

        await call.message.edit_reply_markup(reply_markup=additional_services_kb,
                                             inline_message_id=call.inline_message_id)

    if call.data == 'smooth_cut_500_❌':
        data = await state.get_data()
        await state.update_data(smooth_cut=500)
        if data['cold_regen'] == 0 and data['polishing'] == 0:
            additional_services_kb = await create_additional_services_kb("❌", "❌", "✅")
        elif data['cold_regen'] != 0 and data['polishing'] == 0:
            additional_services_kb = await create_additional_services_kb("✅", "❌", "✅")
        elif data['cold_regen'] == 0 and data['polishing'] != 0:
            additional_services_kb = await create_additional_services_kb("❌", "✅", "✅")
        elif data['cold_regen'] != 0 and data['polishing'] != 0:
            additional_services_kb = await create_additional_services_kb("✅", "✅", "✅")

        await call.message.edit_reply_markup(reply_markup=additional_services_kb,
                                             inline_message_id=call.inline_message_id)
    elif call.data == 'smooth_cut_500_✅':
        data = await state.get_data()
        await state.update_data(smooth_cut=0)
        if data['cold_regen'] == 0 and data['polishing'] == 0:
            additional_services_kb = await create_additional_services_kb("❌", "❌", "❌")
        elif data['cold_regen'] != 0 and data['polishing'] == 0:
            additional_services_kb = await create_additional_services_kb("✅", "❌", "❌")
        elif data['cold_regen'] == 0 and data['polishing'] != 0:
            additional_services_kb = await create_additional_services_kb("❌", "✅", "❌")
        elif data['cold_regen'] != 0 and data['polishing'] != 0:
            additional_services_kb = await create_additional_services_kb("✅", "✅", "❌")

        await call.message.edit_reply_markup(reply_markup=additional_services_kb,
                                             inline_message_id=call.inline_message_id)

    if call.data == 'additional_services_continue':
        await call.message.answer('Процедура выполняеться в первый раз?', reply_markup=first_time_kb)


async def first_time_get_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')

    if call.data == 'first_time_yes':
        await state.update_data(first_time='Да')
    elif call.data == 'first_time_no':
        await state.update_data(first_time='Нет')

    await call.message.answer('Были ли окрашивания, если да, то какое и как часто?',
                              reply_markup=hair_coloring_kb)
    await state.set_state(User.hair_coloring)


async def service_get_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    if call.data == 'ceratin':
        await state.update_data(service='Кератин')
    elif call.data == 'botoks':
        await state.update_data(service='Ботокс')
    elif call.data == 'biskiplastiya':
        await state.update_data(service='Биксипластия')

    await call.message.answer('Выберите <b>длину волос</b>', reply_markup=hair_length_kb)


async def hair_coloring_get_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await state.update_data(hair_coloring='Не было')

    await call.message.answer('Пришлите, пожалуйста, фото волос со спины', reply_markup=unsend_hair_photo_kb)
    await state.set_state(User.hair_photo)


async def hair_photo_get_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await state.update_data(hair_photo='Не захотел')

    await call.message.answer('Укажите номер телефона', reply_markup=specify_phone_kb)
    await state.set_state(User.phone_number)
