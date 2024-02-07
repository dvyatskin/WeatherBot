import os
import sqlite3

from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['delete'])
def delete_history(message: Message) -> None:
    command = 'delete'

    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()
    cur.execute("DELETE FROM history")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, f'История запросов очищена')
