from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def generate_categories(categories):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=category[0])
        buttons.append(btn)
    markup.add(*buttons)
    return markup

def download_button(image_id):
    markup = InlineKeyboardMarkup()
    download = InlineKeyboardButton(text='Скачать изображения', callback_data=f'download_{image_id}')
    markup.add(download)
    return markup
