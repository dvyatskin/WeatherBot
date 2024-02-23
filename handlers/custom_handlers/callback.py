from handlers.custom_handlers.city import get_temp
from handlers.custom_handlers.custom import get_custom_temp
from handlers.custom_handlers.high import get_max_temp
from handlers.custom_handlers.low import get_min_temp
from loader import bot, API
from states.contact_info import WeatherInfoState
from utils.state_code import check


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    req = callback.data.split('_')
    result = check(f'http://api.openweathermap.org/data/2.5/forecast?lat={req[1]}&lon={req[2]}&appid={API}&units=metric')
    if req[3] == 'min':
        bot.set_state(callback.message.from_user.id, WeatherInfoState.minimum, callback.message.chat.id)
        get_min_temp(callback.message, result)
    elif req[3] == 'max':
        bot.set_state(callback.message.from_user.id, WeatherInfoState.maximum, callback.message.chat.id)
        get_max_temp(callback.message, result)
    elif req[3] == 'simple':
        bot.set_state(callback.message.from_user.id, WeatherInfoState.simple, callback.message.chat.id)
        get_temp(callback.message, result)
    elif req[3] == 'custom':
        bot.set_state(callback.message.from_user.id, WeatherInfoState.custom_next, callback.message.chat.id)
        get_custom_temp(callback.message, result, callback.from_user.id)
