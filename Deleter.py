# coding=utf-8

def deleter_key(deleter, c_id):
    delet_key_list = ['location', 'floor', 'district', 'room', 'kl', 'kl_rm', 'type_device', 'device', 'project', 'sp']
    ind_ex = delet_key_list.index(deleter) + 1
    for key in delet_key_list[ind_ex:]:
        if key in c_id:
            c_id.pop(key)
    return c_id

def deleter_backer_checklist(c_id):
    if 'backer_index_count' in c_id['checklist']:
        c_id['checklist'].pop('backer_index_count')
    return c_id
