import os
import sqlite3

from telebot.types import Message

from keyboards.inline.location import loc_keyboard
from loader import bot, API
from states.contact_info import WeatherInfoState
from utils.state_code import check

temp_range = list()


@bot.message_handler(commands=['custom'])
def ask_range(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.custom_range, message.chat.id)
    bot.reply_to(message, 'Выберите диапазон температуры\n(запишите два числа через пробел)')


@bot.message_handler(state=WeatherInfoState.custom_range)
def choose_range(message: Message) -> None:
    global temp_range
    temp_range = message.text.strip().split()
    bot.set_state(message.from_user.id, WeatherInfoState.custom, message.chat.id)
    bot.reply_to(message, 'В каком городе хотите выполнить запрос?')


@bot.message_handler(state=WeatherInfoState.custom)
def choose_city(message: Message) -> None:
    city_name = message.text.strip()

    command = 'custom'
    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()
    cur.execute("INSERT INTO history (command, city) VALUES ('%s', '%s')" % (command, city_name))
    conn.commit()
    cur.close()
    conn.close()

    limit = 3
    result = check(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={API}')
    if result:
        markup = loc_keyboard(result, 'custom')
        bot.send_message(message.chat.id, f'Выберите город:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)


@bot.message_handler(state=WeatherInfoState.custom_next)
def get_custom_temp(message, data) -> None:
    temps = [(data['list'][i]['dt_txt'], data['list'][i]['main']['temp']) for i, i_val in enumerate(data['list'])
             if float(temp_range[0]) <= data['list'][i]['main']['temp'] <= float(temp_range[1])]
    answer = ''
    if temps:
        for i, i_val in enumerate(temps):
            answer += f'Дата: {i_val[0]}, Температура: {i_val[1]}\n'
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, f'Дней с температурой в вашем диапазоне нет')

