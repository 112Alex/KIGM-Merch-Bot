HELLO_TEXT = "Я - бот Колледжа Индустрии Гостеприимства и Менеджмента № 23.\n\nЯ помогу тебе получить официальный мерч нашего колледжа.\n\nЧтобы продолжить, нужно зарегистрироваться"
TEST_USER_LOGIN = "user"
TEST_USER_PASSWORD = "password"
ADMIN_LIST = [5600035106, 1360635951, 6253690850, 781794023]

MAX_EVENT_NAME_LENGTH = 150
MAX_GROUP_LENGTH = 5
MIN_AGE = 14
MAX_AGE = 99

def SHOW_EVENT_TEXT(event_type, event_name, event_date):
    return f'<i>{event_type}</i>\n<strong>{event_name}</strong>\n\n<code>{event_date}</code>'

