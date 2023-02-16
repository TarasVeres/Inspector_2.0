# coding=utf-8
# головний файл, тут відбувається відлов кнопок та сформована логіка що за чим слідує, запускати цей файл
from aiogram import Bot, Dispatcher, types, executor  # імпорти з бібліотеки аіограм
from aiogram.utils.callback_data import CallbackData

import reply_message  # імпорти з внутрішніх файлів
import Deleter
import Inline_Keyboard
import writer
from CheckList import initial_checklist, iter_checklist, request_defect
from Update_Sheet import update_sheet, open_json
from work_data import *

bot = Bot(Token_work, parse_mode=types.ParseMode.HTML)  # вказуємо токен ворк або тест
dp = Dispatcher(bot)
Reply = dict()  # створюємо пустий словарь в який буде збиратись інформація взаємодії з ботом
buy_callback = CallbackData('buy', 'action', 'amount') # тип колбек кнопки, це для фільтрації кнопок по двум різним функціям callback и checklist

@dp.message_handler(commands=['updatesheet']) # функція оновлення данних з таблиці, викликається по команді /updatesheet
async def updatesheet(message: types.Message):
    if message.chat.id == message.from_user.id:
        Sheet = update_sheet()
        if str(message.from_user.id) in Sheet['Access_id']:
            await bot.send_message(chat_id=message.chat.id, text='Данні оновлено. Щоб зробити запис натисніть  /start')
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass


@dp.message_handler(commands=['shiftchange']) # функція редагування робочої зміни в таблиці
async def shift_change(message: types.Message):
    if message.chat.id == message.from_user.id:
        Sheet = open_json()
        if str(message.from_user.id) in Sheet['Access_id']:
            Reply[message.chat.id]['writer_shift'] = ''
            await bot.send_message(message.chat.id, 'Введіть зміну в якій працюєте:')
        await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(commands=['report']) # функція повідомлення про помилку, прилітає словарь з діями що натискав користувач,
# він робить короткий опис помилки і після цього тобі прилітає повідомлення
async def updatesheet(message: types.Message):
    global Reply
    if message.chat.id == message.from_user.id:
        Sheet = open_json()
        if str(message.from_user.id) in Sheet['Access_id']:
            try:
                Reply[message.chat.id]['report'] = ''
                await bot.send_message(message.chat.id, text=f'Логи вашої останньої інспекції будуть переслані @JaneRiabtseva:\n\n'
                                                             f'{Reply[message.chat.id]}')
                await bot.send_message(message.chat.id, text=f'Додайте текст опис помилки, також укажіть на якому зараз етапі знаходитесь\n'
                                                             f'Якщо не бажаєте повідомляти про помилку натисніть /start')
            except KeyError:
                pass

@dp.message_handler(commands=['start'])  # крок1 Відповідь на команду start видаємо кнопки вибір локації
async def start(message: types.Message):
    global Sheet, Reply
    Sheet = open_json()
    if message.chat.id == message.from_user.id:
        if str(message.chat.id) in Sheet['Access_id']:
            m_id = message.chat.id
            Reply[m_id] = dict()
            Reply[m_id]['check_photo'] = ''
            location = [i for i in Sheet['Location']]
            button = Inline_Keyboard.inline_c2_home(location)
            await bot.send_message(message.chat.id, 'На якій локації зафіксовано невідповідність?', reply_markup=button)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.callback_query_handler(buy_callback.filter(action='action')) # функція відлову відповіді від кнопок, все що йде до чеклиста
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
        Reply[c_id]['inspector'] = Sheet['Access_id'][str(call.message.chat.id)][1]
        Reply[c_id]['shift'] = Sheet['Access_id'][str(call.message.chat.id)][2]
        Reply[c_id]['location'] = call_data
        Deleter.deleter_key('location', Reply[c_id])
        Floor = [i for i in Sheet['Location'][Reply[c_id]['location']]]
        button = Inline_Keyboard.inline_c2(Floor, 'Back')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=Reply[c_id]['location'], reply_markup=button)
    elif call_data in Sheet['Location'][Reply[c_id]['location']]: #крок3 обираємо дільницю або девайс якщо склад
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
    elif 'Ajax_Kit' in call_data: # якщо обрали не девайс а  кіти, віддаємо список кітів
        await call.answer(call_data)
        Reply[c_id]['type_device'] = call_data
        Deleter.deleter_key('type_device', Reply[c_id])
        Reply[c_id]['backer'] = Reply[c_id]['district']
        Kit = [i for i in Sheet['kit']]
        button = Inline_Keyboard.inline_c2(Kit, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Оберіть комплект кітів:', reply_markup=button)
    elif call_data in Sheet['kit']: # після вибору кіта віддаємо повідомлених
        await call.answer(call_data)
        Reply[c_id]['kit'] = call_data
        Deleter.deleter_key('device', Reply[c_id])
        Reply[c_id]['backer'] = Reply[c_id]['type_device']
        SP = [i for i in Sheet['SP'][Reply[c_id]['location']][Reply[c_id]['district']]]
        button = Inline_Keyboard.inline_c2(SP, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Повідомлений(на) про невідповідність:', reply_markup=button)
    elif 'Девайс' in call_data: # якщо обрали девайс, віддаємо вибор типу девайса
        await call.answer(call_data)
        Reply[c_id]['backer'] = Reply[c_id]['district']
        Type_device = [i for i in Sheet['Device']]
        button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data, reply_markup=button)
    elif ('non_district' not in Reply[c_id]['floor']) and (call_data in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']]):  # крок4 обираємо робочі місця в середині дільниці
        await call.answer(call_data)
        Reply[c_id]['district'] = call_data
        Deleter.deleter_key('district', Reply[c_id])
        Reply[c_id]['backer'] = Reply[c_id]['floor']
        if (Reply[c_id]['district'] in Sheet['Non_place']) and (call_data not in Sheet['Device&Kit']): # якщо дільниця не потребує вибору роб місця
            Reply[c_id]['room'] = Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']][0]
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
    elif ('non_district' not in Reply[c_id]['floor']) and (call_data in Sheet['Location'][Reply[c_id]['location']][Reply[c_id]['floor']][Reply[c_id]['district']]):  # крок6 обираємо лінійку девайсів
        await call.answer(call_data)
        if call_data in 'Без роб місця':
            Reply[c_id]['backer'] = Reply[c_id]['floor']
            text_message = Reply[c_id]["district"]
        else:
            Reply[c_id]['backer'] = Reply[c_id]['district']
            text_message = f'{Reply[c_id]["district"]} - {call_data}'
        Reply[c_id]['room'] = call_data
        Deleter.deleter_key('room', Reply[c_id])
        Type_device = [i for i in Sheet['Device']]
        button = Inline_Keyboard.inline_c2(Type_device, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text_message, reply_markup=button)
    elif call_data in Sheet['Device']:   # крок7 обираємо девайс
        await call.answer(call_data)
        Reply[c_id]['type_device'] = call_data
        Deleter.deleter_key('type_device', Reply[c_id])
        if 'room' not in Reply[c_id]:
            Reply[c_id]['backer'] = Reply[c_id]['district']
        else:
            Reply[c_id]['backer'] = Reply[c_id]['room']
        if "Без девайсу" in call_data:
            Reply[c_id]['device'] = call_data
            SP = [i for i in Sheet['SP'][Reply[c_id]['location']][Reply[c_id]['district']]]
            button = Inline_Keyboard.inline_c2(SP, Reply[c_id]['backer'])
            text_message = 'Повідомлений(на) про невідповідність:'
        else:
            Device = [i for i in Sheet['Device'][Reply[c_id]['type_device']]]
            button = Inline_Keyboard.inline_c2(Device, Reply[c_id]['backer'])
            text_message = call_data
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text_message, reply_markup=button)
    elif ('kit' not in Reply[c_id]) and (call_data in Sheet['Device'][Reply[c_id]['type_device']]) and (Reply[c_id]['district'] not in Sheet['Non_project']):
             # крок8 обираємо проект
        await call.answer(call_data)
        Reply[c_id]['device'] = call_data
        Deleter.deleter_key('device', Reply[c_id])
        Reply[c_id]['backer'] = Reply[c_id]['type_device']
        Project = [i for i in Sheet['Device'][Reply[c_id]['type_device']][Reply[c_id]['device']]]
        button = Inline_Keyboard.inline_c1(Project, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data, reply_markup=button)
    elif ('kit' not in Reply[c_id]) and (call_data in Sheet['Device'][Reply[c_id]['type_device']]) or (call_data not in Sheet['SP'][Reply[c_id]['location']][Reply[c_id]['district']]) and \
        ((Reply[c_id]['district'] not in Sheet['Non_project']) and (("Без девайсу" not in Reply[c_id]['device']) and
                                    (call_data in Sheet['Device'][Reply[c_id]['type_device']][Reply[c_id]['device']]))):  # крок9 обираємо відповідального
        await call.answer(call_data)
        if Reply[c_id]['district'] in Sheet['Non_project']:
            Reply[c_id]['backer'] = Reply[c_id]['type_device']
            Reply[c_id]['device'] = call_data
        else:
            Reply[c_id]['backer'] = Reply[c_id]['device']
            Reply[c_id]['project'] = call_data
        Deleter.deleter_key('project', Reply[c_id])
        SP = [i for i in Sheet['SP'][Reply[c_id]['location']][Reply[c_id]['district']]]
        button = Inline_Keyboard.inline_c2(SP, Reply[c_id]['backer'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Повідомлений(на) про невідповідність:', reply_markup=button)
    elif (call_data in Sheet['SP'][Reply[c_id]['location']][Reply[c_id]['district']]) and (call_data not in "Відсутній в списку"):
        # після вибору відповідального переходимо де проходу по чеклисту
        await call.answer(call_data)
        if (('device' in Reply[c_id]) and (Reply[c_id]['device'] in "Без девайсу")) or ('project' not in Reply[c_id]):
            Reply[c_id]['backer'] = Reply[c_id]['type_device']
        else:
            Reply[c_id]['backer'] = Reply[c_id]['project']
        Reply[c_id]['sp'] = call_data
        await initial_checklist(Reply[c_id], Sheet, call)
    elif call_data in "Відсутній в списку": #якщо відповідальний був відсутній в списку то вносимо вручну
        await call.answer()
        if 'project' in Reply[c_id]:
            Reply[c_id]['backer'] = Reply[c_id]['project']
        else:
            Reply[c_id]['backer'] = Reply[c_id]['device']
        Reply[c_id]['sp'] = "Відсутній в списку"
        button.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=buy_callback.new(action='action',
                                                                                         amount=Reply[c_id]['backer'])))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Введіть ПІБ працівника повідомленого про невідповідність:', reply_markup=button)
    elif 'change_photo' in call_data: # зміна фото/відео невідповідності якщо відправили помилково не те
        await call.answer()
        Reply[c_id]['check_photo'] = ''
        button.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=buy_callback.new(action='checklist',
                                                                                         amount='backer_photo')))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Зробіть фото/відео невідповідності', reply_markup=button)
    elif call_data in 've_chat': # пересилання постів в чат з записом в таблицю
        await call.answer()
        Reply[c_id]['ve_chat'] = True
        await reply_message.message_ve_chat(Reply[c_id], Chat_work)
        Reply[c_id] = dict()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Повідомлення успішно переслане в чат та записане в таблицю.')
    elif call_data in 'no_ve_chat': # відміна пересилання постів в таблицю
        await call.answer()
        Reply[c_id] = dict()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Залишимо данне повідомлення тут')


@dp.callback_query_handler(buy_callback.filter(action='checklist')) # відлов відповіді від кнопок коли йдемо по чеклисту
async def callback(call: types.CallbackQuery, callback_data: dict):
    global Reply, Sheet, Request, Request_defect
    c_id = call.from_user.id
    call_data = callback_data['amount'].replace('[', '').replace(']', '').split(', ')
    button = types.InlineKeyboardMarkup()
    if  call_data[0] in "'OK'": # якщо відповідь ок
        await call.answer(call_data[0])
        Reply[c_id]['checklist']['log'].append('OK')
        Reply[c_id]['checklist']['Time_inspection'] += [call_data[1]]
        Reply[c_id]['checklist']['Rating'] += [call_data[2]]
        Reply[c_id]['checklist']['Rating_all'] += [call_data[2]]
        Deleter.deleter_backer_checklist(Reply[c_id])
        await iter_checklist(Reply[c_id], Sheet, call)
    elif call_data[0] in "'NOK'": # якщо відповідь нок
        await call.answer(call_data[0])
        Reply[c_id]['check_photo'] = ''
        Reply[c_id]['checklist']['log'].append('NOK')
        Reply[c_id]['checklist']['Time_inspection'] += [call_data[1]]
        Reply[c_id]['checklist']['Rating_all'] += [call_data[2]]
        Deleter.deleter_backer_checklist(Reply[c_id])
        button.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=buy_callback.new(action='checklist', amount='backer_photo')))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Зробіть фото/відео невідповідності", reply_markup=button)
    elif call_data[0] in "'N/A'": # якщо відповідь N/A
        await call.answer(call_data[0])
        Reply[c_id]['checklist']['log'].append('N/A')
        Deleter.deleter_backer_checklist(Reply[c_id])
        await iter_checklist(Reply[c_id], Sheet, call)
    elif ('backer_checklist' in call_data[0]) or ('backer_photo' in call_data[0]): # якщо під час проходу по чеклисту на якомусь питанню повертаємось назад
        await call.answer()
        if Reply[c_id]['checklist']['log'][-1] == 'OK':
            Reply[c_id]['checklist']['Time_inspection'].pop()
            Reply[c_id]['checklist']['Rating_all'].pop()
            Reply[c_id]['checklist']['Rating'].pop()
        elif Reply[c_id]['checklist']['log'][-1] == 'NOK':
            Reply[c_id]['checklist']['Time_inspection'].pop()
            Reply[c_id]['checklist']['Rating_all'].pop()
        Reply[c_id]['checklist']['log'].pop()
        if 'backer_checklist' in call_data[0]:
            Reply[c_id]['checklist']['index_count'] -= 2
        elif 'backer_photo' in call_data[0]:
            Reply[c_id]['checklist']['index_count'] -= 1
        await iter_checklist(Reply[c_id], Sheet, call)
    elif 'checklist_text' in call_data[0]: # повернення назад після опису невідповідності
        await call.answer()
        Request_defect, output_defect_message = request_defect(Reply[c_id])
        Request = Reply[c_id]['checklist']
        Request[Request_defect]['text'] = ''
        button.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=buy_callback.new(action='action',
                                                                                         amount='change_photo')))
        await bot.send_message(chat_id=call.message.chat.id, text='Зробіть короткий опис невідповідності:', reply_markup=button)
    elif call_data[0] in Sheet['Location'][Reply[c_id]['location']]: # обір поверху генератору невідповідності
        await call.answer(f'Локація: {call_data[0]}')
        Request_defect, output_defect_message = request_defect(Reply[c_id])
        Request = Reply[c_id]['checklist']
        if 'non_district' in Sheet['Location'][Reply[c_id]['location']][call_data[0]]:  # якщо без поверха склад або щось на одному рівні з поверхом
            Request[Request_defect]['floor'] = 'non_district'
            Request[Request_defect]['district'] = call_data[0]
            await iter_checklist(Reply[c_id], Sheet, call)
        else:
            Request[Request_defect]['floor'] = call_data[0]
            District = [i for i in Sheet['Location'][Reply[c_id]['location']][Request[Request_defect]['floor']]]
            button = Inline_Keyboard.inline_c2Checklist(District, 'checklist_text')
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=call_data[0], reply_markup=button)
    elif call_data[0] in Sheet['Location'][Reply[c_id]['location']][Request[Request_defect]['floor']]: #крок3 обираємо дільницю або девайса якщо склад
        await call.answer(call_data[0])
        Request[Request_defect]['backer'] = Request[Request_defect]['floor']
        Request[Request_defect]['district'] = call_data[0]
        await iter_checklist(Reply[c_id], Sheet, call)

@dp.message_handler(content_types=['text']) # відлов текстових повідомлень
async def handle_files(message):
    try:
        if message.chat.id == message.from_user.id:
            Sheet = open_json()
            if str(message.chat.id) in Sheet['Access_id']:
                m_id = Inline_Keyboard.func_message(message)[0]
                text = Inline_Keyboard.func_message(message)[1]
                if 'report' in Reply[m_id]: # після вибору повідомлення про помилку і вказання короткого опису її
                    Reply[m_id]['report'] = text
                    await bot.send_message(message.chat.id, text='Повідомлення про помилку відправлено.')
                    await bot.send_message(chat_id=207451670, text=Reply[m_id])
                elif "Відсутній в списку" in Reply[m_id]['sp']: # якщо необхідно вказати сп який був відсутній в списку
                    Reply[m_id]['sp'] = text
                    await initial_checklist(Reply[m_id], Sheet, call=message)
                elif ('checklist' in Reply[m_id]) and ('photos'in Reply[m_id]['checklist'][Reply[m_id]['checklist']['Request_message'][len(Reply[m_id]['checklist']['log'])-1].split('\n')[2]]):
                    # опис невідповідності після отриманого фото
                    Request_defect, output_defect_message = request_defect(Reply[m_id])
                    if Reply[m_id]['checklist'][Request_defect]['text'] == '':
                        Reply[m_id]['checklist'][Request_defect]['text'] = text
                        Reply[m_id]['checklist'][Request_defect]['floor'] = ''
                        Floor = [i for i in Sheet['Location'][Reply[m_id]['location']]]
                        Reply[m_id]['backer'] = 'checklist_text'
                        button = Inline_Keyboard.inline_c2Checklist(Floor, Reply[m_id]['backer'])
                        await bot.send_message(chat_id=message.chat.id, text='Оберіть дільницю генератор невідповідності:', reply_markup=button)
                elif 'writer_shift' in Reply[m_id]:
                    writer.writer_shift(Reply[m_id], text, Sheet)
                    Reply[m_id]['inspector'] = Sheet['Access_id'][str(message.chat.id)][1]
                    post = f"Редагування зміни успішно завершено:\n{Reply[m_id]['inspector']} - {text} зміна."
                    await bot.send_message(chat_id=message.chat.id, text=post)
    except KeyError:
        pass


@dp.message_handler(content_types=['video', 'photo']) # відлов фото та відео матеріалів
async def start_function(message: types.Message):
    global Request_defect
    if message.chat.id == message.from_user.id:
        if str(message.chat.id) in Sheet['Access_id']:
            m_id = message.chat.id
            if ('checklist' in Reply[m_id]) and (Reply[m_id]['checklist']['log'][-1] == 'NOK'):
                if Reply[m_id]['check_photo'] == '':
                    Request_defect, output_defect_message = request_defect(Reply[m_id])
                    Reply[m_id]['checklist'][Request_defect] = dict()
                    Reply[m_id]['checklist'][Request_defect]['output_defect_message'] = output_defect_message
                    Reply[m_id]['checklist'][Request_defect]['photos'] = []
                    Reply[m_id]['checklist'][Request_defect]['videos'] = []
                    Reply[m_id]['checklist'][Request_defect]['med'] = []
                    Reply[m_id]['checklist'][Request_defect]['text'] = ''
                try:
                    Reply[m_id]['checklist'][Request_defect]['photos'].append(message.photo[0].file_id)
                except (KeyError, IndexError):
                    pass
                try:
                    Reply[m_id]['checklist'][Request_defect]['videos'].append(message.video.file_id)
                except AttributeError:
                    pass
                    if Reply[m_id]['check_photo'] == '':
                        Reply[m_id]['check_photo'] = message.media_group_id
                        button = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Змінити фото/відео',
                                 callback_data=buy_callback.new(action='action', amount='change_photo')),
                                 types.InlineKeyboardButton('⬅️ Назад', callback_data=buy_callback.new(action='checklist', amount='backer_photo')))
                        await bot.send_message(message.chat.id, text='Зробіть короткий опис невідповідності:',
                                               reply_markup=button)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=False)
