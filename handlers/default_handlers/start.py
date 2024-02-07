import sqlite3
import os

from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    command = 'start'

    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS history (id int auto_increment primary key, command varchar, city varchar)')
    cur.execute("INSERT INTO history (command, city) VALUES ('%s', '%s')" % (command, '-'))
    conn.commit()
    cur.close()
    conn.close()

    bot.reply_to(message, f"Привет, {message.from_user.first_name}!")
