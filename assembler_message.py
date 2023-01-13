import time

import matrix


def assembler_good(c_id, Sheet):
    text = f'{time.strftime("%d.%m.%Y", time.localtime())}\n' \
           f'Проведено інспекцію на локації: {c_id["location"]}, {c_id["floor"]}'
    if c_id['floor'] not in Sheet['Storage']:
        text += f'\nДільниця: {c_id["district"]}'
    if ('room' in c_id) and (("Без р.м." not in c_id['room']) or ("Без роб місця" not in c_id['room'])):
        text += f', {c_id["room"]}'
    else:
        text += f', зміна{c_id["zmina"]}\n'
    text += f'Невідповідностей виявлено не було. Результат - 100 %.\n' \
            f'Повідомлений(на): {c_id["sp"]}\n'\
            f'Провів(ла) інспекцію: {c_id["reported"]}\n'\
            f'Ви (вогник)!'
    return text

def assembler_false(c_id, Sheet):
    text = f'{time.strftime("%d.%m.%Y", time.localtime())}\n' \
           f'Проведено інспекцію на локації: {c_id["location"]}, {c_id["floor"]}'
    if c_id['floor'] not in Sheet['Storage']:
        text += f'\nДільниця: {c_id["district"]}'
    if ('room' in c_id) and (("Без р.м." not in c_id['room']) or ("Без роб місця" not in c_id['room'])):
        text += f', {c_id["room"]}'
    else:
        text += f', зміна{c_id["zmina"]}\n'
    text += f'Виявлено невідповідностей {matrix.count_false(c_id)}. Результат: {matrix}%.\n' \
            f'Повідомлений(на): {c_id["sp"]}\n' \
            f'Провів(ла) інспекцію: {c_id["reported"]}\n' \
            f'Ви можете краще!'