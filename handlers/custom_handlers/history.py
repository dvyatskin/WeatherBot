import os
import sqlite3

from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['history'])
def request_history(message: Message) -> None:
    command = 'history'

    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()
    cur.execute('SELECT * FROM history')
    requests = cur.fetchall()

    info = ''
    for i in requests[-1:-11:-1]:
        if i[1].startswith('без') is False:
            info += f'/{i[1]} : {i[2]}\n'
        else:
            info += f'None command : {i[2]}\n'
    cur.close()
    conn.close()

    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()
    cur.execute("INSERT INTO history (command, city) VALUES ('%s', '%s')" % (command, '-'))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, f'Последние 10 запросов:\n{info}')
