from aiogram import types
from aiogram.utils.callback_data import CallbackData

import reply_message


def import_bot():
    from Inspector_2 import bot
    return bot

buy_callback = CallbackData('buy', 'action', 'amount')
# action - параметр сортування колбеків
# amount - данні які передаються з колбеком

async def initial_checklist(c_id, Sheet, call):
    c_id['checklist'] = {}
    c_id['checklist']['Request_message'] = []
    c_id['checklist']['Time_inspection'] = []
    c_id['checklist']['Rating'] = []
    c_id['checklist']['log'] = []
    for Type_defect in Sheet['CheckList'][c_id['district']].keys():
        for Request in Sheet['CheckList'][c_id['district']][Type_defect].keys():
            f_str = f'{Type_defect}\n-----------\n{Request}'
            c_id['checklist']['Request_message'].append(f_str)
    await iter_checklist(c_id, Sheet, call)

async def iter_checklist(c_id, Sheet, call):
    global Type_defect, Request_defect
    bot = import_bot()
    Request = c_id['checklist']['Request_message']
    if 'index_count' in c_id['checklist']:
        ind_ex = c_id['checklist']['index_count']
    else:
        ind_ex = 0
    try:
        Type_defect = Request[ind_ex].split('\n')[0]
        Request_defect = Request[ind_ex].split('\n')[2]
    except IndexError:
        await reply_message.message(c_id, call, Sheet)
    Request_defect_checklist = Request[ind_ex - 1].split('\n')[2]
    while True:
        try:
            Request_message = Request[ind_ex]
        except IndexError:
            break
        ind_ex += 1
        Time_inspection = Sheet['CheckList'][c_id['district']][Type_defect][Request_defect]['time_inspection']
        Rating = Sheet['CheckList'][c_id['district']][Type_defect][Request_defect]['rating']
        c_id['checklist']['index_count'] = ind_ex
        if (ind_ex == 1) or (c_id['checklist']['index_count'] == 1):
            if 'project' in c_id:
                inline_backer = ['action', c_id['project']]
            else:
                if 'kit' in c_id:
                    inline_backer = ['action', c_id['kit']]
                else:
                    inline_backer = ['action', c_id['device']]
        elif Request_defect_checklist in c_id['checklist']:
            inline_backer = ['checklist', c_id['checklist'][Request_defect_checklist]['floor']]
        else:
            inline_backer = ['checklist', 'backer_checklist']
        button = button_cheklist(Time_inspection, Rating, inline_backer)
        try:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=Request_message, reply_markup=button)
        except AttributeError:
            await bot.send_message(chat_id=call.chat.id, text=Request_message, reply_markup=button)
        break

def button_cheklist(Time_inspection, Rating, inline_backer):
    button = types.InlineKeyboardMarkup(row_width=2)
    button.add(
        types.InlineKeyboardButton('OK', callback_data=buy_callback.new(action='checklist',
                                                                   amount=['OK', Time_inspection, Rating])),
        types.InlineKeyboardButton('NOK',
                                   callback_data=buy_callback.new(action='checklist', amount=['NOK', Time_inspection, Rating]))
    )
    button.add(
        types.InlineKeyboardButton('N/A', callback_data=buy_callback.new(action='checklist', amount=['N/A', Time_inspection, Rating])),
        types.InlineKeyboardButton('⬅️ Назад', callback_data=buy_callback.new(action=inline_backer[0], amount=inline_backer[1]))
    )
    return button

def request_defect(c_id):
    Request = c_id['checklist']['Request_message']
    Request_defect = Request[len(c_id['checklist']['log'])-1].split('\n')[2]
    output_defect_message = Request[len(c_id['checklist']['log'])-1].split('\n')[0]
    return Request_defect, output_defect_message