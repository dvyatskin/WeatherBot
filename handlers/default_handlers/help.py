import os
import sqlite3

from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    command = 'help'

    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()
    cur.execute("INSERT INTO history (command, city) VALUES ('%s', '%s')" % (command, '-'))
    conn.commit()
    cur.close()
    conn.close()

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
