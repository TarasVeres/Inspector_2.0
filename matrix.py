def count_false(c_id):
    c_id = c_id['checklist']
    count_defect = len(c_id['checklist']['log'])
    return count_defect