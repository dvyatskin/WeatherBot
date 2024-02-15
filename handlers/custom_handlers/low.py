import os
import sqlite3

from telebot.types import Message

from database.db_insert import one_insert
from keyboards.inline.location import loc_keyboard
from loader import bot, API
from states.contact_info import WeatherInfoState
from utils.state_code import check


@bot.message_handler(commands=['low'])
def ask_city_name(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.low, message.chat.id)
    bot.reply_to(message, 'В каком городе хотите найти минимальную температуру')


@bot.message_handler(state=WeatherInfoState.low)
def choose_city(message: Message) -> None:
    city_name_min = message.text.strip()
    command = 'low'

    one_insert(command, city_name_min)

    limit = 3
    result = check(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name_min}&limit={limit}&appid={API}')
    if result:
        markup = loc_keyboard(result, 'min')
        bot.send_message(message.chat.id, f'Выберите город:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)


@bot.message_handler(state=WeatherInfoState.minimum)
def get_min_temp(message, data) -> None:
    temps = [data['list'][i]['main']['temp'] for i, i_val in enumerate(data['list'])]
    min_temp = min(temps)
    for i, i_val in enumerate(data['list']):
        if data['list'][i]['main']['temp'] == min_temp:
            date = data['list'][i]['dt_txt']
    bot.send_message(message.chat.id, f'Минимальная температура в течение 5 дней будет\n{date}\n'
                                      f'составит: {min_temp} граудса')

