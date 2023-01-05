# coding=utf-8
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.callback_data import CallbackData
import pprint

import writer
import Deleter
import Inline_Keyboard
import assembler_message
from CheckList import initial_checklist, iter_checklist
from Update_Sheet import update_sheet, open_json

Token_work = '5388966053:AAE6rJo_7wbBbGDMG3QntbjN549Ym1lyEgY'
Chat_work = '-1001286473377'

Token_test = '5182014508:AAEBytjLM9Gu-3F2o1Qc2QPt5bwdvNWxFEk'
Chat_test = '-1001626029923'

bot = Bot(Token_test, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
Reply = dict()
buy_callback = CallbackData('buy', 'action', 'amount')

@dp.message_handler(commands=['updatesheet'])
async def updatesheet(message: types.Message):
    if message.chat.id == message.from_user.id:
        Sheet = update_sheet()
        if str(message.from_user.id) in Sheet['Access_id']:
            await bot.send_message(chat_id=message.chat.id, text='Данні з таблиці оновлено.')
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(commands=['start'])  # крок1 Відповідь на команду start видаємо кнопки вибір локації
async def start(message: types.Message):
    global Sheet, Reply
    Sheet = open_json()
    if message.chat.id == message.from_user.id:
        if str(message.chat.id) in Sheet['Access_id']:
            m_id = message.chat.id
            Reply[m_id] = dict()
            location = [i for i in Sheet['Location']]
            button = Inline_Keyboard.inline_c2_home(location)
            await bot.send_message(message.chat.id, 'На якій локації зафіксовано невідповідність?', reply_markup=button)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.callback_query_handler(buy_callback.filter(action='action'))
async def callback(call: types.CallbackQuery, callback_data: dict):
    global Reply, Sheet
    button = types.InlineKeyboardMarkup(row_width=2)
    c_id = call.from_user.id
    call_data = callback_data["amount"]
    if (call_data in Sheet['Location']) and not Sheet['Location'][call_data]:  # Відповідь на випадок якщо локація ще пуста
        await call.answer(f'Локація: {call_data}')
        button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=buy_callback.new(action='action', amount='Back')))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Локація ще будується!', reply_markup=button)
    elif call_data in 'Back':  # крок1 повернення на початок, обираємо локацію
        await call.answer(text='')
        location = [i for i in Sheet['Location']]
        button = Inline_Keyboard.inline_c2_home(location)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='На якій локації зафіксовано невідповідність?', reply_markup=button)
    elif call_data in Sheet['Location']:  # крок2 обираємо поверх або склад
        await call.answer(f'Локація: {call_data}')
        Reply[c_id]['location'] = call_data
        Deleter.deleter_key('location', Reply[c_id])
        Floor = [i for i in Sheet['Location'][Reply[c_id]['location']]]
        button = Inline_Keyboard.inline_c2(Floor, 'Back')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=Reply[c_id]['location'], reply_markup=button)
    elif (call_data in Sheet['Location'][Reply[c_id]['location']]): #крок3 обираємо дільницю або девайса якщо склад
        await call.answer(call_data)
        Reply[c_id]['backer'] = Reply[c_id]['location']
        if 'non_district' in Sheet['Location'][Reply[c_id]['location']][call_data]:  # якщо без поверха склад або щось на одному рівні з поверхом
            Reply[c_id]['floor'] = 'non_district'
            Reply[c_id]['district'] = call_data
            Deleter.deleter_key('district', Reply[c_id])
            if call_data in Sheet['Device&Kit']:  # якщо це склад готової продукціїї і можуть бути кіти або девайси
                button.add(
                    types.InlineKeyboardButton(text='Девайс', callback_data=buy_callback.new(action='action', amount='Девайс')),
                    types.InlineKeyboardButton(text='Kit', callback_data=buy_callback.new(action='action', amount='Ajax_Kit'))
                )
                button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=buy_callback.new(action='action', amount=Reply[c_id]['backer'])))
            else:  # обираємо девайси якщо це склад або щось на рівні з поверхом але не кіти
                Type_device = [i for i in Sheet['Device']]
                button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
        else: # поверх
            Reply[c_id]['floor'] = call_data
            Deleter.deleter_key('floor', Reply[c_id])
            district = [i for i in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']]]
            button = Inline_Keyboard.inline_c2(district, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data, reply_markup=button)
    elif call_data in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']]:  # крок4 обираємо робочі місця в середині дільниці
        await call.answer(call_data)
        Reply[c_id]['district'] = call_data
        Deleter.deleter_key('district', Reply[c_id])
        Reply[c_id]['backer'] = Reply[c_id]['floor']
        if Reply[c_id]['district'] in Sheet['Non_place']: # якщо дільниця не потребує вибору роб місця
            Reply[c_id]['room'] = Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']][0]
            Deleter.deleter_key('room', Reply[c_id])
            Type_device = [i for i in Sheet['Device']]
            button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
        elif Reply[c_id]['district'] in Sheet['Device&Kit']: # якщо дільниця мастербокс і потребує вибору девайси чи кіти
            button.add(
                types.InlineKeyboardButton(text='Девайс', callback_data=buy_callback.new(action='action', amount='Девайс')),
                types.InlineKeyboardButton(text='Kit', callback_data=buy_callback.new(action='action', amount='Ajax_Kit'))
            )
            button.add(
                types.InlineKeyboardButton(text='⬅️ Назад', callback_data=buy_callback.new(action='action', amount=Reply[c_id]['backer'])))
        else:  # якщо дільниця потребує вибір роб місця
            Place = [i for i in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']]]
            button = Inline_Keyboard.inline_c2(Place, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data, reply_markup=button)
    elif call_data in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']]:  # крок6 обираємо лінійку девайсів
        await call.answer(call_data)
        Reply[c_id]['backer'] = Reply[c_id]['district']
        Reply[c_id]['room'] = call_data
        Deleter.deleter_key('room', Reply[c_id])
        Type_device = [i for i in Sheet['Device']]
        button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{Reply[c_id]["district"]} - {call_data}', reply_markup=button)
    elif call_data in Sheet['Device']:   # крок7 обираємо девайс
        await call.answer(call_data)
        Reply[c_id]['type_device'] = call_data
        Deleter.deleter_key('type_device', Reply[c_id])
        Reply[c_id]['text_message'] = call_data
        if 'kl_rm' in Reply[c_id]:
            Reply[c_id]['backer'] = Reply[c_id]['kl_rm']
        else:
            Reply[c_id]['backer'] = Reply[c_id]['room']
        if "Без девайсу" in call_data:
            await initial_checklist(Reply[c_id], Sheet, call)
        else:
            Device = [i for i in Sheet['Device'][Reply[c_id]['type_device']]]
            button = Inline_Keyboard.inline_c2(Device, Reply[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data, reply_markup=button)
    elif call_data in Sheet['Device'][Reply[c_id]['type_device']]:  # крок8 обираємо проект
        await call.answer(call_data)
        Reply[c_id]['device'] = call_data
        Deleter.deleter_key('device', Reply[c_id])
        Reply[c_id]['backer'] = Reply[c_id]['type_device']
        Project = [i for i in Sheet['Device'][Reply[c_id]['type_device']][Reply[c_id]['device']]]
        button = Inline_Keyboard.inline_c1(Project, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data, reply_markup=button)
    elif call_data in Sheet['Device'][Reply[c_id]['type_device']][Reply[c_id]['device']]:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        await call.answer(call_data)
        Reply[c_id]['backer'] = Reply[c_id]['device']
        Reply[c_id]['project'] = call_data
        Deleter.deleter_key('project', Reply[c_id])
        button.add(types.InlineKeyboardButton(text='Nazad', callback_data=buy_callback.new(action='action', amount=Reply[c_id]['backer'])))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data, reply_markup=button)

@dp.callback_query_handler(buy_callback.filter(action='checklist'))
async def callback(call: types.CallbackQuery, callback_data: dict):
    global Reply, Sheet
    try:
        c_id = call.from_user.id
        call_data = callback_data['amount'].replace('[', '').replace(']', '').split(', ')
        if  call_data[0] in "'OK'":
            await call.answer(call_data[0])
            Reply[c_id]['checklist']['Time_inspection'] += call_data[1]
            Reply[c_id]['checklist']['Rating'] += call_data[2]
            await iter_checklist(Reply[c_id], Sheet, call)
        elif call_data[0] in "'NOK'":
            await call.answer(call_data[0])
            Reply[c_id]['checklist']['Time_inspection'] += call_data[1]
            await iter_checklist(Reply[c_id], Sheet, call)
        elif call_data[0] in "'N/A'":
            await call.answer(call_data[0])
            await iter_checklist(Reply[c_id], Sheet, call)
        # elif 'backer' in call.message.text:
        pprint.pprint(Reply)
    except ZeroDivisionError:
        pass



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=False)
