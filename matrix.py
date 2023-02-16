def count_false(c_id):
    count_defect = c_id['checklist']['log'].count('NOK')
    return count_defect

def count_result(c_id):
    count = sum([int(i) for i in c_id['checklist']['Rating_all']])
    count_ok = sum([int(i) for i in c_id['checklist']['Rating']])
    result = int(count_ok / count * 100)
    return result

def count_time_inspection(c_id):
    setap = [int(i) for i in c_id['checklist']['Time_inspection']]
    count = sum(setap)
    if count >= 60:
        count = f'{count // 60}год {count % 60}хв'
    else:
        count = f'{count % 60}хв'
    return count