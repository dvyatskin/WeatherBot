from telebot.types import Message

from loader import bot, API
import requests
import json
from states.contact_info import WeatherInfoState


@bot.message_handler(commands=['high'])
def choose_city(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.high, message.chat.id)
    bot.reply_to(message, 'Выберите город в котором хотите найти максимальную температуру')


@bot.message_handler(state=WeatherInfoState.high)
def get_max_temp(message: Message) -> None:
    city_name_max = message.text.strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name_max}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'Максимальная температура в городе {city_name_max}:\n'
                              f'tmax={round(data["main"]["temp_max"], 1)}')
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)