from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    bot.reply_to(message, f"Привет, {message.from_user.first_name}!")


# @bot.message_handler(content_types=['text'])
# def say_hello(message: Message) -> None:
#     if 'привет' in message.text.lower():
#         bot.reply_to(message, f"Привет, {message.from_user.first_name}!")
