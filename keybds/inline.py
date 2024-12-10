from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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

YES_NO_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="да", callback_data='yes'), InlineKeyboardButton(text="нет", callback_data='no')],
])

def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()

SEND_REQUEST = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="отметить участие", callback_data='send_request')],
]) #TODO в data должны передаваться данные о конкретном мероприятии (id мероприятие должен доставаться по названию)