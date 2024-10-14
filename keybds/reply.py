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
    [KeyboardButton(text="Волонтёрство во время проведения чемпионатов и т.д. (1день)")],
    [KeyboardButton(text="Волонтёрское мероприятие за пределами колледжа (1день)")],
    [KeyboardButton(text="Участие в творческих мероприятиях колледжа (небольшое)")],
    [KeyboardButton(text="Участие в творческих мероприятиях колледжа (масштабное)")],
    [KeyboardButton(text="Участие в мероприятих города, представляя колледж")],
    [KeyboardButton(text="Участие в чемпионатах профессионального мастерства")],
    [KeyboardButton(text="Отличная учёба (учёт за семестр)")],
    [KeyboardButton(text="Участие в благотворительных акциях, квизах и блицах")],
    [KeyboardButton(text="Участие в спортивных мероприятиях внутри колледжа")],
    [KeyboardButton(text="Участие в спортивных мероприятиях, представляя колледж")],
], resize_keyboard=True, one_time_keyboard=True)
