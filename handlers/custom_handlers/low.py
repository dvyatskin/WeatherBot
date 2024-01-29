from telebot.types import Message
from telebot import types

from keyboards.inline.location import loc_keyboard
from loader import bot, API
import requests
import json
from states.contact_info import WeatherInfoState


@bot.message_handler(commands=['low'])
def choose_city(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.low, message.chat.id)
    bot.reply_to(message, 'Выберите город в котором хотите найти минимальную температуру')


@bot.message_handler(state=WeatherInfoState.low)
def get_min_temp(message: Message) -> None:
    city_name_min = message.text.strip()
    limit = 3
    res = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name_min}&limit={limit}&appid={API}')
    if res.status_code == 200:
        # data = res.json()
        # markup = types.InlineKeyboardMarkup()
        # btn1 = types.InlineKeyboardButton(f'{data[0]["name"]}, {data[0]["country"]}', callback_data='first')
        # markup.row(btn1)
        # btn2 = types.InlineKeyboardButton(f'{data[1]["name"]}, {data[1]["country"]}', callback_data='second')
        # btn3 = types.InlineKeyboardButton(f'{data[2]["name"]}, {data[2]["country"]}', callback_data='third')
        # markup.row(btn2, btn3)
        markup = loc_keyboard([0, 1, 2])
        bot.send_message(message.chat.id, f'Выберите город:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'first':
        bot.send_message(callback.message.chat.id, 'Первый')
    elif callback.data == 'second':
        bot.send_message(callback.message.chat.id, 'ВТорой')
    elif callback.data == 'third':
        bot.send_message(callback.message.chat.id, 'Третий')
    #     bot.reply_to(message, f'Минимальная температура в городе {city_name_min}:\n'
    #                           f'tmin={round(data["main"]["temp_min"], 1)}')
    # else:
    #     bot.reply_to(message, 'Город не найден')
    # bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)
