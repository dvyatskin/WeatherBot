from telebot.handler_backends import State, StatesGroup


class WeatherInfoState(StatesGroup):
    city = State()
    low = State()
    high = State()
