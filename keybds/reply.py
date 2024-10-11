from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

AUTH_BTN = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="зарегистрироваться", callback_data='reg')],
    [InlineKeyboardButton(text="авторизироваться", callback_data='auth')],
])

ADMIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="добавить мероприятие", callback_data='add_event')],
    [InlineKeyboardButton(text="посмотреть список мероприятий", callback_data='show_events')],
    [InlineKeyboardButton(text="посмотреть заявки", callback_data='show_applications')],
    [InlineKeyboardButton(text="включить магазин", callback_data='run_shop')],
    [InlineKeyboardButton(text="отключить магазин", callback_data='stop_shop')],
])

MENU_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="посмотреть список мероприятий", callback_data='show_events')],
    [InlineKeyboardButton(text="узнать количество баллов", callback_data='show_score')],
    [InlineKeyboardButton(text="посмотреть ассортимент", callback_data='show_assortment')],
])

ADD_EVENT_KEYBOARD = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Волонтёрское благотворительное мероприятие в колледже")],
    [KeyboardButton(text="Небельное волонтёрское мероприятие в колледже")],
    [KeyboardButton(text="Волонтёрское мероприятие в колледже")],
], resize_keyboard=True, one_time_keyboard=True)
