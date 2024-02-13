from telebot.handler_backends import State, StatesGroup


class WeatherInfoState(StatesGroup):
    city = State()
    low = State()
    high = State()
    custom = State()
    custom_range = State()
    custom_next = State()
    minimum = State()
    maximum = State()
    simple = State()

