# coding=utf-8

from aiogram import Bot, Dispatcher, types, executor

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
Reply_message = dict()


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
    global Sheet, reply_message
    Sheet = open_json()
    if message.chat.id == message.from_user.id:
        if str(message.chat.id) in Sheet['Access_id']:
            m_id = message.chat.id
            Reply_message[m_id] = dict()
            location = [i for i in Sheet['Location']]
            button = Inline_Keyboard.inline_c2_home(location)
            await bot.send_message(message.chat.id, 'На якій локації зафіксовано невідповідність?', reply_markup=button)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.callback_query_handler(lambda callback_query: True)
async def callback(call: types.CallbackQuery):
    global Reply_message, Sheet
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
            Reply_message[c_id]['location'] = call.data
            Floor = [i for i in Sheet['Location'][Reply_message[c_id]['location']]]
            button = Inline_Keyboard.inline_c2(Floor, 'Back')
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=Reply_message[c_id]['location'], reply_markup=button)
        elif (call.data in Sheet['Location'][Reply_message[c_id]['location']]): #крок3 обираємо дільницю або девайса якщо склад
            await call.answer(call.data)
            Reply_message[c_id]['backer'] = Reply_message[c_id]['location']
            if 'non_distric' in Sheet['Location'][Reply_message[c_id]['location']][call.data]:  # якщо без поверха склад або щось на одному рівні з поверхом
                Reply_message[c_id]['floor'] = 'non_distric'
                Reply_message[c_id]['distric'] = call.data
                Reply_message[c_id]['project'] = 'non_project'
                if 'Production Warehouse' in Reply_message[c_id]['distric']:  # якщо це склад готової продукціїї і можуть бути кіти або девайси
                    button.add(
                        types.InlineKeyboardButton(text='Девайс', callback_data='Девайс'),
                        types.InlineKeyboardButton(text='Kit', callback_data='Ajax_Kit')
                    )
                    button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply_message[c_id]['backer']))
                else:  # обираємо девайси якщо це склад або щось на рівні з поверхом але не кіти
                    Device = [i for i in Sheet['Device']]
                    button = Inline_Keyboard.inline_c2(Device, Reply_message[c_id]['backer'])
            else: # поверх
                Reply_message[c_id]['floor'] = call.data
                Distric = [i for i in Sheet['Location'][Reply_message[c_id]['location']][Reply_message[c_id]['floor']]]
                button = Inline_Keyboard.inline_c2(Distric, Reply_message[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.data, reply_markup=button)
        elif call.data in Sheet['Location'][Reply_message[c_id]['location']][Reply_message[c_id]['floor']]:  # крок4 обираємо робочі місця в середині дільниці
            await call.answer(call.data)
            Reply_message[c_id]['distric'] = call.data
            Reply_message[c_id]['backer'] = Reply_message[c_id]['floor']
            if Reply_message[c_id]['distric'] in Sheet['Non_place']: # якщо дільниця не потребує вибору роб місця
                Device = [i for i in Sheet['Device']]
                button = Inline_Keyboard.inline_c2(Device, Reply_message[c_id]['backer'])
            elif 'non_project' in Sheet['Location'][Reply_message[c_id]['location']][Reply_message[c_id]['floor']][Reply_message[c_id]['distric']]:  # якщо дільниця не потребує вибору проекта
                Reply_message[c_id]['project'] = 'non_project'
                if Reply_message[c_id]['distric'] in Sheet['Non_standart']:  # якщо дільниця не потребує вибору проекта і роб місця
                    if 'Master' in Reply_message[c_id]['distric']:  # якщо дільниця мастербокс і потребує вибору девайси чи кіти
                        button.add(
                            types.InlineKeyboardButton(text='Девайс', callback_data='Девайс'),
                            types.InlineKeyboardButton(text='Kit', callback_data='Ajax_Kit')
                        )
                        button.add(
                            types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply_message[c_id]['backer']))
                    else:
                        Device = [i for i in Sheet['Device']]
                        button = Inline_Keyboard.inline_c2(Device, Reply_message[c_id]['backer'])
                else:  # якщо дільниця не потребує вибору проекта але потребує вибір роб місця
                    Place = [i for i in Sheet['Location'][Reply_message[c_id]['location']][Reply_message[c_id]['floor']][Reply_message[c_id]['distric']]['non_project']]
                    button = Inline_Keyboard.inline_c2(Place, Reply_message[c_id]['backer'])
            else:  # якщо дільниця потребує вибір роб місця
                Place = [i for i in Sheet['Location'][Reply_message[c_id]['location']][Reply_message[c_id]['floor']][Reply_message[c_id]['distric']]]
                button = Inline_Keyboard.inline_c2(Place, Reply_message[c_id]['backer'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.data, reply_markup=button)
        elif call.data in Sheet['Location'][Reply_message[c_id]['location']][Reply_message[c_id]['floor']][Reply_message[c_id]['distric']]:  # крок5 обираємо лінійку девайсів
            await call.answer(call.data)
            Reply_message[c_id]['backer'] = Reply_message[c_id]['distric']
            if Reply_message[c_id]['distric'] in Sheet['Room']:
                Reply_message[c_id]['room'] = call.data
                Device = [i for i in Sheet['Device']]
                button = Inline_Keyboard.inline_c2(Device, Reply_message[c_id]['backer'])
            elif Reply_message[c_id]['distric'] in Sheet['KL_line']:
                KL_line = [i for i in Sheet['KL_R_M']]
                button = Inline_Keyboard.inline_c2(KL_line, Reply_message[c_id]['backer'])
            else:


    except ZeroDivisionError:
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=False)
