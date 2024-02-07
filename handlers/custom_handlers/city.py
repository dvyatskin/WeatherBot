import os
import sqlite3

from telebot.types import Message

from keyboards.inline.location import loc_keyboard
from loader import bot, API
from states.contact_info import WeatherInfoState
from utils.state_code import check


@bot.message_handler(commands=['city'])
def ask_city_name(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.city, message.chat.id)
    bot.reply_to(message, 'В каком городе хотите посмотреть погоду')


@bot.message_handler(state=WeatherInfoState.city)
def get_weather(message: Message) -> None:
    city_name = message.text.strip()

    command = 'low'

    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()
    cur.execute("INSERT INTO history (command, city) VALUES ('%s', '%s')" % (command, city_name))
    conn.commit()
    cur.close()
    conn.close()

    limit = 3
    result = check(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={API}')
    if result:
        markup = loc_keyboard(result, 'simple')
        bot.send_message(message.chat.id, f'Выберите город:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)


@bot.message_handler(state=WeatherInfoState.simple)
def get_temp(message, data) -> None:

    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)
    bot.send_message(message.chat.id, f'Сейчас погода:'
                                      f'на улице - {data["list"][0]["weather"][0]["main"]}\n'
                                      f'температура {round(data["list"][0]["main"]["temp"], 1)}, '
                                      f'ощущается как {round(data["list"][0]["main"]["feels_like"], 1)}')
