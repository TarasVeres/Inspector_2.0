# coding=utf-8
from aiogram import types
from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData('buy', 'action', 'amount')

def inline_c2(data, backer):
    button = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(data), 2):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=buy_callback.new(action='action', amount=data[i])),
                types.InlineKeyboardButton(text=data[i + 1], callback_data=buy_callback.new(action='action', amount=data[i + 1]))
            )
        except IndexError:
            button.add(types.InlineKeyboardButton(text=data[i], callback_data=buy_callback.new(action='action', amount=data[i])),
                       types.InlineKeyboardButton(text='⬅️ Назад', callback_data=buy_callback.new(action='action', amount=backer))
            )
        else:
            if data[i + 1] == data[-1]:
                button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=buy_callback.new(action='action', amount=backer)))
    return button


def inline_c1(data, backer):
    button = types.InlineKeyboardMarkup(row_width=1)
    for i in range(0, len(data)):
        button.add(types.InlineKeyboardButton(text=data[i], callback_data=buy_callback.new(action='action', amount=data[i])))
    button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=buy_callback.new(action='action', amount=backer)))
    return button


def inline_c2_home(data):
    button = types.InlineKeyboardMarkup()
    for i in range(0, len(data), 2):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=buy_callback.new(action='action', amount=data[i])),
                types.InlineKeyboardButton(text=data[i + 1], callback_data=buy_callback.new(action='action', amount=data[i + 1]))
            )
        except IndexError:
            button.add(types.InlineKeyboardButton(text=data[i], callback_data=buy_callback.new(action='action', amount=data[i])))
    return button


def func_message(message):
    message_id = message.from_user.id
    message_txt = message.text
    return message_id, message_txt