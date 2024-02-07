from telebot import types


def loc_keyboard(data, mode):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(f'{data[0]["name"]}, {data[0]["country"]}',
                                      callback_data=f'first_{data[0]["lat"]}_{data[0]["lon"]}_{mode}')
    markup.row(btn1)
    if len(data) == 2:
        btn2 = types.InlineKeyboardButton(f'{data[1]["name"]}, {data[1]["country"]}',
                                          callback_data=f'second_{data[1]["lat"]}_{data[1]["lon"]}_{mode}')
        if len(data) == 3:
            btn3 = types.InlineKeyboardButton(f'{data[2]["name"]}, {data[2]["country"]}',
                                              callback_data=f'third_{data[2]["lat"]}_{data[2]["lon"]}_{mode}')
            markup.row(btn2, btn3)
        else:
            markup.row(btn2)
    return markup
