from aiogram import Dispatcher, executor, Bot
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
import os
import sqlite3
from keyboards import *
import random
import re

load_dotenv()
TOKEN=os.getenv('TOKEN')

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer('Привет! Здесь ты найдеш щбщи на любой вкус!!!')
    await show_categories(message)


async def show_categories(message: Message):
    database = sqlite3.connect('wallpaper.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT category_name FROM categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    await message.answer('Выберить категорию', reply_markup=generate_categories(categories))


@dp.message_handler(content_types=['text'])
async def get_image(message: Message):
    database = sqlite3.connect('wallpaper.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT image_link FROM images WHERE category_id = (
        (
            SELECT category_id FROM categories WHERE category_name = ?
        )
    )
    ''', (message.text, ))
    image_links = cursor.fetchall()
    try:

        random_image_link = random.choice(image_links)[0]
        print(random_image_link)

        cursor.execute('''
        SELECT image_id FROM images WHERE image_link = ? 
        ''', (random_image_link, ))
        image_id = cursor.fetchone()[0]
        database.close()

        resolution = re.search(r'[0-9]+x[0-9]+', random_image_link)[0]
        try:
            await message.answer_photo(photo=random_image_link,
                                       caption=f'''Разришения: {resolution}''', reply_markup=download_button(image_id))
        except Exception as e:
            print(e)
            image_resize_link = random_image_link.replace(resolution, '1920x1080')
            await message.answer_photo(photo=image_resize_link,
                                       caption=f'''Разришения: {resolution}''', reply_markup=download_button(image_id))

    except:
        pass


@dp.callback_query_handler(lambda call: 'download' in call.data)
async def download_function(call: CallbackQuery):
    _, image_id = call.data.split('_')
    database = sqlite3.connect('wallpaper.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT image_link FROM images WHERE image_id = ?
    ''', (image_id, ))
    image_link = cursor.fetchone()[0]
    database.close()

    chat_id = call.message.chat.id

    await bot.send_document(chat_id, document=image_link)


executor.start_polling(dp)