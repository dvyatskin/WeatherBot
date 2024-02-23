from telebot.types import Message

from database.db_in import create_history
from keyboards.inline.location import loc_keyboard
from loader import bot, API
from states.contact_info import WeatherInfoState
from utils.state_code import check


@bot.message_handler(commands=['high'])
def ask_city_name(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.high, message.chat.id)
    bot.reply_to(message, 'В каком городе хотите найти максимальную температуру')


@bot.message_handler(state=WeatherInfoState.high)
def get_weather(message: Message) -> None:
    city_name = message.text.strip()
    user_id = message.from_user.id
    command = 'high'
    create_history(user_id, command, city_name)

    limit = 3
    result = check(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={API}')
    if result:
        markup = loc_keyboard(result, 'max')
        bot.send_message(message.chat.id, f'Выберите город:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)


@bot.message_handler(state=WeatherInfoState.maximum)
def get_max_temp(message, data) -> None:
    temps = [data['list'][i]['main']['temp'] for i, i_val in enumerate(data['list'])]
    max_temp = max(temps)
    for i, i_val in enumerate(data['list']):
        if data['list'][i]['main']['temp'] == max_temp:
            date = data['list'][i]['dt_txt']
    bot.send_message(message.chat.id, f'Максимальная температура в течение 5 дней будет\n{date}\n'
                                      f'составит: {max_temp} граудса')
