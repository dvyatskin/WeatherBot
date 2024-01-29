from telebot import types


def loc_keyboard(data):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(f'{data[0]}', callback_data='first')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton(f'{data[1]}', callback_data='second')
    btn3 = types.InlineKeyboardButton(f'{data[2]}', callback_data='third')
    markup.row(btn2, btn3)
    return markup
