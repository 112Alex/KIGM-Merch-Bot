from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


AUTH_BTN = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="зарегистрироваться", callback_data='reg')],
])

ADMIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="добавить мероприятие", callback_data='add_event')],
    [InlineKeyboardButton(text="посмотреть список мероприятий", callback_data='show_events')],
    [InlineKeyboardButton(text="посмотреть заявки", callback_data='show_applications')],
])

YES_NO_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="да", callback_data='yes'), InlineKeyboardButton(text="нет", callback_data='no')],
])

ADD_SCORE = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начислить баллы", callback_data='add_score')]
])

def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()