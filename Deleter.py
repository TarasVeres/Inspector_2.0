# coding=utf-8

def deleter_key(deleter, c_id):
    delet_key_list = ['location', 'floor', 'district', 'room', 'kl', 'kl_rm', 'type_device', 'device', 'project']
    ind_ex = delet_key_list.index(deleter) + 1
    for key in delet_key_list[ind_ex:]:
        if key in c_id:
            c_id.pop(key)
    return c_id

async def CheckList(c_id, Sheet, dp, call):
    for Type_defect in Sheet['CheckList']['SMT'].keys():
        for Request in Sheet['CheckList']['SMT'][Type_defect]:
            text_message = f'{Type_defect}\n--------\n{Request}'
