from database.models import User, History

from telebot.types import Message

from database.db_in import create_user, create_history
from loader import bot


@bot.message_handler(commands=["history"])
def bot_start(message: Message) -> None:

    user_id = message.from_user.id
    command = 'history'

    user = User.get(User.user_id == user_id)
    user_histories = user.histories.order_by(History.history_id.desc()).limit(10)
    text = [f"/{i.command} : {i.city}" for i in user_histories]
    full_text = '\n'.join(text)
    bot.send_message(message.chat.id, f'Последние 10 запросов:\n{full_text}')

    create_history(user_id, command, '-')
