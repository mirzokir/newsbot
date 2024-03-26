from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def generate_categories(lst: list):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    category_buttons = []

    for category in lst:
        btn = KeyboardButton(text=category)
        category_buttons.append(btn)

    back = KeyboardButton(text='◀️назад')
    category_buttons.append(back)
    markup.add(*category_buttons)
    return markup


def generate_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Погода')
    markup.add(btn)
    return markup


def generate_button1():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Ob-xavo🌤')
    markup.add(btn)
    return markup
