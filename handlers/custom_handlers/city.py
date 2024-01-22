from telebot.types import Message

from loader import bot, API
import requests
import json
from states.contact_info import WeatherInfoState


@bot.message_handler(commands=['city'])
def choose_city(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.city, message.chat.id)
    bot.reply_to(message, 'Выберите город в котором хотите посмотреть погоду')


@bot.message_handler(state=WeatherInfoState.city)
def get_weather(message: Message) -> None:
    city_name = message.text.strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'Сейчас погода в городе {city_name}:\n'
                              f'на улице - {data["weather"][0]["main"]}\n'
                              f'температура {round(data["main"]["temp"], 1)}, ощущается как {round(data["main"]["feels_like"], 1)}')
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)