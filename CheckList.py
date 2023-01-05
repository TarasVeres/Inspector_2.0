from aiogram import types
from aiogram.utils.callback_data import CallbackData

def import_bot():
    from Inspector_2 import bot
    return bot

buy_callback = CallbackData('buy', 'action', 'amount')
# action - параметр сортування колбеків
# amount - данні які передаються з колбеком

async def initial_checklist(c_id, Sheet, call):
    c_id['checklist'] = {}
    c_id['checklist']['Type_defect'] = []
    c_id['checklist']['Request'] = []
    c_id['checklist']['Time_inspection'] = []
    c_id['checklist']['Rating'] = []
    for Type_defect in Sheet['CheckList'][c_id['district']].keys():
        c_id['checklist']['Type_defect'].append(Type_defect)
        list_Request = []
        for Request in Sheet['CheckList'][c_id['district']][Type_defect].keys():
            list_Request.append(Request)
        c_id['checklist']['Request'].append(list_Request)
    await iter_checklist(c_id, Sheet, call)

async def iter_checklist(c_id, Sheet, call):
    Type_defect = c_id['checklist']['Type_defect']
    Request = c_id['checklist']['Request']
    if 'index_count' in c_id['checklist']:
        ind_ex = c_id['checklist']['index_count']
        count_Type_defect, count_Request, count_Request_inside = ind_ex[0], ind_ex[1], ind_ex[2]
    else:
        count_Type_defect, count_Request, count_Request_inside = 0, 0, -1
    while True:
        count_Request_inside += 1
        try:
            Type_defect_while = Type_defect[count_Type_defect]
        except IndexError:
            break
        try:
            Request_while = Request[count_Request][count_Request_inside]
        except IndexError:
            count_Type_defect += 1
            count_Request += 1
            count_Request_inside = -1
            continue
        Time_inspection = Sheet['CheckList'][c_id['district']][Type_defect_while][Request_while]['time_inspection']
        Rating = Sheet['CheckList'][c_id['district']][Type_defect[count_Type_defect]][Request[count_Request][count_Request_inside]]['rating']
        text_message = f'{Type_defect_while}\n -----------\n {Request_while}'
        c_id['checklist']['index_count'] = [count_Type_defect, count_Request, count_Request_inside]
        button = button_cheklist(Time_inspection, Rating, )
        bot = import_bot()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=text_message, reply_markup=button)
        break

def button_cheklist(Time_inspection, Rating):
    button = types.InlineKeyboardMarkup(row_width=2)
    button.add(
        types.InlineKeyboardButton('OK', callback_data=buy_callback.new(action='checklist',
                                                                   amount=['OK', Time_inspection, Rating])),
        types.InlineKeyboardButton('NOK',
                                   callback_data=buy_callback.new(action='checklist', amount=['NOK', Time_inspection, Rating]))
    )
    button.add(
        types.InlineKeyboardButton('N/A', callback_data=buy_callback.new(action='checklist', amount=['N/A', Time_inspection, Rating])),
        types.InlineKeyboardButton('⬅️ Назад', callback_data=buy_callback.new(action='checklist', amount='backer'))
    )
    return button