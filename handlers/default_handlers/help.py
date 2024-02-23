from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from database.db_in import create_history
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    user_id = message.from_user.id
    command = 'help'
    text = [f"/{command} -{desk}" for command, desk in DEFAULT_COMMANDS]
    full_text = "\n".join(text)
    bot.reply_to(message, f'Рад что ты спросил 🤓\n\n{full_text}')

    create_history(user_id, command, '-')
