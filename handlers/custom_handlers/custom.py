from telebot.types import Message

from database.db_in import create_history, create_custom
from database.models import User, Custom
from keyboards.inline.location import loc_keyboard
from loader import bot, API
from states.contact_info import WeatherInfoState
from utils.state_code import check


@bot.message_handler(commands=['custom'])
def ask_range(message: Message) -> None:
    bot.set_state(message.from_user.id, WeatherInfoState.custom_range, message.chat.id)
    bot.reply_to(message, 'Выбери диапазон температур.\n'
                          'Введи минимум🥶 и максимум🥵 через пробел.')


@bot.message_handler(state=WeatherInfoState.custom_range)
def choose_range(message: Message) -> None:
    user_id = message.from_user.id
    temp_range = message.text.strip().split()
    if len(temp_range) == 2:
        create_custom(user_id, temp_range[0], temp_range[1])
        bot.set_state(message.from_user.id, WeatherInfoState.custom, message.chat.id)
        bot.reply_to(message, 'В каком городе хотите выполнить запрос?')
    else:
        bot.reply_to(message, 'Диапазон введен неверно...🫠')
        bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)


@bot.message_handler(state=WeatherInfoState.custom)
def choose_city(message: Message) -> None:
    city_name = message.text.strip()
    user_id = message.from_user.id
    command = 'custom'
    create_history(user_id, command, city_name)

    limit = 3
    result = check(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={API}')
    if result:
        markup = loc_keyboard(result, 'custom')
        bot.send_message(message.chat.id, f'Выберите город:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Город не найден')
    bot.set_state(message.from_user.id, WeatherInfoState, message.chat.id)


@bot.message_handler(state=WeatherInfoState.custom_next)
def get_custom_temp(message, data, user_id=None) -> None:
    user = User.get(User.user_id == user_id)
    user_customs = user.customs.order_by(Custom.custom_id.desc()).limit(1)

    temps = [(data['list'][i]['dt_txt'], data['list'][i]['main']['temp']) for i, i_val in enumerate(data['list'])
             if float(user_customs[0].temp_min) <= data['list'][i]['main']['temp'] <= float(user_customs[0].temp_max)]
    answer = ''
    if temps:
        for i, i_val in enumerate(temps):
            answer += f'Дата: {i_val[0]}, Температура: {i_val[1]}\n'
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, f'Дней с температурой в вашем диапазоне нет')

