# coding=utf-8
from aiogram import types

def inline_c2(data, backer):
    button = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(data), 2):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                types.InlineKeyboardButton(text=data[i + 1], callback_data=data[i + 1])
            )
        except IndexError:
            button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                       types.InlineKeyboardButton(text='⬅️ Назад', callback_data=backer))
        else:
            if data[i + 1] == data[-1]:
                button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=backer))
    return button


def inline_c1(data, backer):
    button = types.InlineKeyboardMarkup(row_width=1)
    for i in range(0, len(data)):
        button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]))
    button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=backer))
    return button


def inline_c2_home(data):
    button = types.InlineKeyboardMarkup()
    for i in range(0, len(data), 2):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                types.InlineKeyboardButton(text=data[i + 1], callback_data=data[i + 1])
            )
        except IndexError:
            button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]))
    return button


def func_message(message):
    message_id = message.from_user.id
    message_txt = message.text
    return message_id, message_txt