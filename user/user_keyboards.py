from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main_menu_but = [
    [InlineKeyboardButton(text='🛍️Записаться', callback_data="order_main_menu")],
]

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=main_menu_but)

unsend_hair_photo_but = [
    [InlineKeyboardButton(text='Не присылать', callback_data="unsend_hair_photo")],
]

unsend_hair_photo_kb = InlineKeyboardMarkup(inline_keyboard=unsend_hair_photo_but)


hair_length_but = [
    [InlineKeyboardButton(text='До плеч 3000₽', callback_data="hair_length_3000")],
    [InlineKeyboardButton(text='До лопаток 3500₽', callback_data="hair_length_3500")],
    [InlineKeyboardButton(text='Ниже лопаток 4000₽', callback_data="hair_length_4000")],
    [InlineKeyboardButton(text='До талии 4500₽', callback_data="hair_length_4500")],
    [InlineKeyboardButton(text='Ниже талии 5000₽', callback_data="hair_length_5000")],
    [InlineKeyboardButton(text='До колен 8000₽', callback_data="hair_length_8000")],
]

hair_length_kb = InlineKeyboardMarkup(inline_keyboard=hair_length_but)

hair_density_but = [
    [InlineKeyboardButton(text='Не густые 0₽', callback_data="hair_density_0")],
    [InlineKeyboardButton(text='Средняя густота 500₽', callback_data="hair_density_500")],
    [InlineKeyboardButton(text='Очень густые 1000₽', callback_data="hair_density_1000")],
]

hair_density_kb = InlineKeyboardMarkup(inline_keyboard=hair_density_but)

service_but = [
    [InlineKeyboardButton(text='Кератин', callback_data="ceratin")],
    [InlineKeyboardButton(text='Ботокс', callback_data="botoks")],
    [InlineKeyboardButton(text='Биксипластия', callback_data="biskiplastiya")],
]

service_kb = InlineKeyboardMarkup(inline_keyboard=service_but)

first_time_but = [
    [
        InlineKeyboardButton(text='Да', callback_data="first_time_yes"),
        InlineKeyboardButton(text='Нет', callback_data="first_time_no")
     ]
]

first_time_kb = InlineKeyboardMarkup(inline_keyboard=first_time_but)

hair_coloring_but = [
    [InlineKeyboardButton(text='Не было', callback_data="hair_coloring_no")]
]

hair_coloring_kb = InlineKeyboardMarkup(inline_keyboard=hair_coloring_but)


specify_phone_but = [
    [KeyboardButton(text="☎️Указать номер телефона", request_contact=True)]
]

specify_phone_kb = ReplyKeyboardMarkup(
    keyboard=specify_phone_but,
    resize_keyboard=True,
    input_field_placeholder="Укажите номер телефона"
)


async def create_additional_services_kb(cold_regen, polishing, smooth_cut):
    additional_services_but = [
        [InlineKeyboardButton(text=f'Холодное восстановление 1500₽ {cold_regen}', callback_data=f"cold_regen_1500_{cold_regen}")],
        [InlineKeyboardButton(text=f'Полировка 1000₽ {polishing}', callback_data=f"polishing_1000_{polishing}")],
        [InlineKeyboardButton(text=f'Ровный срез 500₽ {smooth_cut}', callback_data=f"smooth_cut_500_{smooth_cut}")],
        [InlineKeyboardButton(text='Дальше', callback_data="additional_services_continue")],
    ]

    additional_services_kb = InlineKeyboardMarkup(inline_keyboard=additional_services_but)

    return additional_services_kb
