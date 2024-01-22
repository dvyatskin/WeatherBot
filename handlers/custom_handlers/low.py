from telebot.types import Message

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
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name_min}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'Минимальная температура в городе {city_name_min}:\n'
                              f'tmin={round(data["main"]["temp_min"], 1)}')
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)