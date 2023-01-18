import assembler_message
from aiogram import types

import writer


def import_bot():
    from Inspector_2 import bot, buy_callback
    return bot, buy_callback




async def message(c_id, call, Sheet):
    bot, buy_callback = import_bot()
    if 'NOK' not in c_id['checklist']['log']:
        text = assembler_message.assembler_good(c_id, Sheet)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text)
        await reply_button_ve_chat(buy_callback, bot, call)
    else:
        text = assembler_message.assembler_false(c_id, Sheet)
        del_data_log = ['Time_inspection', 'Rating', 'log', 'Request_message', 'index_count']
        data_log = [i for i in c_id['checklist'] if i not in del_data_log]
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
        for l in data_log:
            data = c_id['checklist'][l]
            text_false = assembler_message.assembler_false_count(c_id, data)
            for i in data['photos']:
                if i != data['photos'][-1]:
                    data['med'].append(types.InputMediaPhoto(media=i))
                else:
                    data['med'].append(
                        types.InputMediaPhoto(media=i, caption=text_false))
            for i in data['videos']:
                if data['photos']:
                    data['med'].append(types.InputMediaVideo(media=i))
                else:
                    if i != data['videos'][-1]:
                        data['med'].append(types.InputMediaVideo(media=i))
                    else:
                        data['med'].append(
                            types.InputMediaVideo(media=i, caption=text_false))
            await bot.send_media_group(call.message.chat.id, media=data['med'])
        await reply_button_ve_chat(buy_callback, bot, call)

async def message_ve_chat(c_id, call, Sheet):
    bot, buy_callback = import_bot()
    if 'NOK' not in c_id['checklist']['log']:
        text = assembler_message.assembler_good(c_id, Sheet)
        await bot.send_message(chat_id=call, text=text)
    else:
        text = assembler_message.assembler_false(c_id, Sheet)
        del_data_log = ['Time_inspection', 'Rating', 'log', 'Request_message', 'index_count']
        data_log = [i for i in c_id['checklist'] if i not in del_data_log]
        await bot.send_message(chat_id=call, text=text)
        for l in data_log:
            data = c_id['checklist'][l]
            await bot.send_media_group(chat_id=call, media=data['med'])
            writer.writer_false(c_id, data)
    writer.writer_result(c_id)

async def reply_button_ve_chat(buy_callback, bot, call):
        button = types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton('Так', callback_data=buy_callback.new(action='action', amount='ve_chat')),
            types.InlineKeyboardButton('Hi', callback_data=buy_callback.new(action='action', amount='no_ve_chat')),
            types.InlineKeyboardButton('⬅️ Назад',
                                       callback_data=buy_callback.new(action='checklist', amount='backer_checklist'))
        )
        await bot.send_message(call.message.chat.id, text='Переслати повідомлення в чат?', reply_markup=button)