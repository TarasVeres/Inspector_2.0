# файл збирання кінцевого повідомлення, як він буде виглядати в телеграмі

import time

import matrix


def assembler_good(c_id): # головне повідомлення якщо інспекція була без невідповідностей
    text = f'{time.strftime("%d.%m.%Y", time.localtime())}\n' \
           f'Проведено інспекцію на локації: {c_id["location"]}'
    if 'non_district' not in c_id['floor']:
           text += f', {c_id["floor"]}'
    text += f'\nДільниця: {c_id["district"]}'
    if ('room' in c_id) and (("Без р.м." not in c_id['room']) and ("Без роб місця" not in c_id['room'])):
        text += f', {c_id["room"]}'
    text += f', зміна - {c_id["shift"]}\n'
    text += f'Невідповідностей виявлено не було. Результат - 100%.\n' \
            f'Повідомлений(на): {c_id["sp"]}\n'\
            f'Провів(ла) інспекцію: {c_id["inspector"]}\n'\
            f'Ви 🔥!'
    return text

def assembler_false(c_id): # головне повідомлення якщо інспекція була з невідповідностями
    text = f'{time.strftime("%d.%m.%Y", time.localtime())}\n' \
           f'Проведено інспекцію на локації: {c_id["location"]}'
    if 'non_district' not in c_id['floor']:
           text += f', {c_id["floor"]}'
    text += f'\nДільниця: {c_id["district"]}'
    if ('room' in c_id) and (("Без р.м." not in c_id['room']) and ("Без роб місця" not in c_id['room'])):
        text += f', {c_id["room"]}'
    text += f', зміна - {c_id["shift"]}\n'
    text += f'Виявлено невідповідностей: {matrix.count_false(c_id)}. Результат: {matrix.count_result(c_id)}%.\n' \
            f'Повідомлений(на): {c_id["sp"]}\n' \
            f'Провів(ла) інспекцію: {c_id["inspector"]}\n' \
            f'Ви можете краще!'
    return text

def assembler_false_count(c_id, Request_defect): # формування повідомлень з невідповідностями
    text = f'{time.strftime("%d.%m.%Y", time.localtime())}\n'
    if 'project' in c_id:
        text += f'Плата: {c_id["project"]}\n'
    else:
        if 'kit' in c_id:
            text += f'Kit: {c_id["kit"]}\n'
        elif 'Без девайсу' not in c_id['device']:
            text += f'Девайс: {c_id["device"]}\n'
    text += f'Група невідповідності: {Request_defect["output_defect_message"]}\n'\
    f'Генератор невідповідності: {Request_defect["district"]}\n'\
    f'Опис невідповідності: {Request_defect["text"]}\n'\
    f'Зафіксував(ла): {c_id["inspector"]}'
    return text