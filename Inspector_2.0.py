# coding=utf-8

from aiogram import Bot, Dispatcher, types, executor
import pprint

import writer
import Deleter
import Inline_Keyboard
import assembler_message
from Update_Sheet import update_sheet, open_json

Token_work = '5388966053:AAE6rJo_7wbBbGDMG3QntbjN549Ym1lyEgY'
Chat_work = '-1001286473377'

Token_test = '5182014508:AAEBytjLM9Gu-3F2o1Qc2QPt5bwdvNWxFEk'
Chat_test = '-1001626029923'

bot = Bot(Token_test, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
Reply = dict()


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

@dp.callback_query_handler(lambda callback_query: True)
async def callback(call: types.CallbackQuery):
    global Reply, Sheet
    button = types.InlineKeyboardMarkup(row_width=2)
    try:
        c_id = call.from_user.id
        if (call.data in Sheet['Location']) and not Sheet['Location'][call.data]:  # Відповідь на випадок якщо локація ще пуста
            await call.answer(f'Локація: {call.data}')
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='Back'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Локація ще будується!', reply_markup=button)
        elif call.data in 'Back':  # крок1 повернення на початок, обираємо локацію
            await call.answer(text='')
            location = [i for i in Sheet['Location']]
            button = Inline_Keyboard.inline_c2_home(location)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='На якій локації зафіксовано невідповідність?', reply_markup=button)
        elif call.data in Sheet['Location']:  # крок2 обираємо поверх або склад
            await call.answer(f'Локація: {call.data}')
            Reply[c_id]['location'] = call.data
            Deleter.deleter_key('location', Reply[c_id])
            Floor = [i for i in Sheet['Location'][Reply[c_id]['location']]]
            button = Inline_Keyboard.inline_c2(Floor, 'Back')
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=Reply[c_id]['location'], reply_markup=button)
        elif (call.data in Sheet['Location'][Reply[c_id]['location']]): #крок3 обираємо дільницю або девайса якщо склад
            await call.answer(call.data)
            Reply[c_id]['backer'] = Reply[c_id]['location']
            if 'non_district' in Sheet['Location'][Reply[c_id]['location']][call.data]:  # якщо без поверха склад або щось на одному рівні з поверхом
                Reply[c_id]['floor'] = 'non_district'
                Reply[c_id]['district'] = call.data
                Deleter.deleter_key('district', Reply[c_id])
                if 'Production Warehouse' in Reply[c_id]['district']:  # якщо це склад готової продукціїї і можуть бути кіти або девайси
                    button.add(
                        types.InlineKeyboardButton(text='Девайс', callback_data='Девайс'),
                        types.InlineKeyboardButton(text='Kit', callback_data='Ajax_Kit')
                    )
                    button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply[c_id]['backer']))
                else:  # обираємо девайси якщо це склад або щось на рівні з поверхом але не кіти
                    Type_device = [i for i in Sheet['Device']]
                    button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
            else: # поверх
                Reply[c_id]['floor'] = call.data
                Deleter.deleter_key('floor', Reply[c_id])
                district = [i for i in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']]]
                button = Inline_Keyboard.inline_c2(district, Reply[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.data, reply_markup=button)
        elif call.data in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']]:  # крок4 обираємо робочі місця в середині дільниці
            await call.answer(call.data)
            Reply[c_id]['district'] = call.data
            Deleter.deleter_key('district', Reply[c_id])
            Reply[c_id]['backer'] = Reply[c_id]['floor']
            if Reply[c_id]['district'] in Sheet['Non_place']: # якщо дільниця не потребує вибору роб місця
                Reply[c_id]['room'] = Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']][0]
                Deleter.deleter_key('room', Reply[c_id])
                Type_device = [i for i in Sheet['Device']]
                button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
            elif (Reply[c_id]['district'] in Sheet['Non_standart']) and ('Master' in Reply[c_id]['district']): # якщо дільниця мастербокс і потребує вибору девайси чи кіти
                button.add(
                    types.InlineKeyboardButton(text='Девайс', callback_data='Девайс'),
                    types.InlineKeyboardButton(text='Kit', callback_data='Ajax_Kit')
                )
                button.add(
                    types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply[c_id]['backer']))
            else:  # якщо дільниця потребує вибір роб місця
                Place = [i for i in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']]]
                button = Inline_Keyboard.inline_c2(Place, Reply[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.data, reply_markup=button)
        elif call.data.startswith('КЛ') and (call.data in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']]):    # крок5 обираємо місце на конвеєрі
            await call.answer(call.data)
            Reply[c_id]['backer'] = Reply[c_id]['district']
            Reply[c_id]['kl'] = call.data
            Deleter.deleter_key('kl', Reply[c_id])
            KL_RM = [i for i in Sheet["KL_R_M"]]
            button = Inline_Keyboard.inline_c2(KL_RM, Reply[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{Reply[c_id]["district"]} - {call.data}', reply_markup=button)
        elif (call.data in Sheet["KL_R_M"]) or ((not call.data.startswith('КЛ')) and
            (call.data in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']])):  # крок6 обираємо лінійку девайсів
            await call.answer(call.data)
            if call.data in Sheet["KL_R_M"]:
                Reply[c_id]['backer'] = Reply[c_id]['kl']
                Reply[c_id]['kl_rm'] = call.data
                Deleter.deleter_key('kl_rm', Reply[c_id])
                f_str = f'{Reply[c_id]["district"]} - {Reply[c_id]["kl"]} - {call.data}'
            else:
                Reply[c_id]['backer'] = Reply[c_id]['district']
                Reply[c_id]['room'] = call.data
                Deleter.deleter_key('room', Reply[c_id])
                f_str = f'{Reply[c_id]["district"]} - {call.data}'
            Type_device = [i for i in Sheet['Device']]
            button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f_str, reply_markup=button)
        elif call.data in Sheet['Device']:   # крок7 обираємо девайс
            await call.answer(call.data)
            Reply[c_id]['type_device'] = call.data
            Deleter.deleter_key('type_device', Reply[c_id])
            if 'kl_rm' in Reply[c_id]:
                Reply[c_id]['backer'] = Reply[c_id]['kl_rm']
            else:
                Reply[c_id]['backer'] = Reply[c_id]['room']
            if "Без девайсу" in call.data:
                Deleter.CheckList(Reply[c_id], Sheet, dp, call)
            else:
                Device = [i for i in Sheet['Device'][Reply[c_id]['type_device']]]
                button = Inline_Keyboard.inline_c2(Device, Reply[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.data, reply_markup=button)
        elif call.data in Sheet['Device'][Reply[c_id]['type_device']]:  # крок8 обираємо проект
            await call.answer(call.data)
            Reply[c_id]['device'] = call.data
            Deleter.deleter_key('device', Reply[c_id])
            Reply[c_id]['backer'] = Reply[c_id]['type_device']
            Project = [i for i in Sheet['Device'][Reply[c_id]['type_device']][Reply[c_id]['device']]]
            button = Inline_Keyboard.inline_c1(Project, Reply[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.data, reply_markup=button)
        elif call.data in Sheet['Device'][Reply[c_id]['type_device']][Reply[c_id]['device']]:
            await call.answer(call.data)
            Reply[c_id]['backer'] = Reply[c_id]['device']
            Reply[c_id]['project'] = call.data
            Deleter.deleter_key('project', Reply[c_id])
            button.add(types.InlineKeyboardButton(text='Nazad', callback_data=Reply[c_id]['backer']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.data, reply_markup=button)
        elif

        pprint.pprint(Reply[c_id])

    except ZeroDivisionError:  #NameError
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=False)
