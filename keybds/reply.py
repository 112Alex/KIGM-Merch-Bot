from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


SHOW_MENU_KB = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Узнать количество баллов")],
    [KeyboardButton(text="Купить мерч")],
    [KeyboardButton(text="Получить баллы")],
], resize_keyboard=True, one_time_keyboard=False)

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
    [KeyboardButton(text="Участие в благотворительных акциях, квизах и блицах")],
    [KeyboardButton(text="Участие в спортивных мероприятиях внутри колледжа")],
    [KeyboardButton(text="Участие в спортивных мероприятиях, представляя колледж")],
], resize_keyboard=True, one_time_keyboard=True)

events = [
    "Волонтёрское благотворительное мероприятие в колледже",
    "Небельное волонтёрское мероприятие в колледже",
    "Волонтёрское мероприятие в колледже",
    "Волонтёрство во время проведения чемпионатов и т.д. (1день)",
    "Волонтёрское мероприятие за пределами колледжа (1день)",
    "Участие в творческих мероприятиях колледжа (небольшое)",
    "Участие в творческих мероприятиях колледжа (масштабное)",
    "Участие в мероприятих города, представляя колледж",
    "Участие в чемпионатах профессионального мастерства",
    "Участие в благотворительных акциях, квизах и блицах",
    "Участие в спортивных мероприятиях внутри колледжа",
    "Участие в спортивных мероприятиях, представляя колледж"
]

# CONTACT_KEYBOARD = ReplyKeyboardMarkup(keyboard=[
#         [KeyboardButton(text="📱 Отправить")]
#     ], request_contact=True,resize_keyboard=True, one_time_keyboard=True)