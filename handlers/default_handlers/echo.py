import os
import sqlite3

from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    command = 'без состояния'

    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()
    cur.execute("INSERT INTO history (command, city) VALUES ('%s', '%s')" % (command, message.text))
    conn.commit()
    cur.close()
    conn.close()

    bot.reply_to(
        message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )
