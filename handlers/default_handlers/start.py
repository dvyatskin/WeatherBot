from telebot.types import Message

from database.db_in import create_user, create_history
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    command = 'start'

    answer = create_user(user_id, username, first_name)
    if answer:
        bot.reply_to(message, f"Добро пожаловать!🌤️\nЯ бот, который умеет определять погоду в любом месте! 🌦️")
    else:
        bot.reply_to(message, f'Рад снова вас видеть, {first_name}!🌤️')

    create_history(user_id, command, '-')
