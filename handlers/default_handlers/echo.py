import os
import sqlite3

from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):

    bot.reply_to(
        message, f"Извините, я вас не понимаю!🤕\n"
                 f"Чтобы узнать меня поближе, воспользуйтесь командой /help"
    )
