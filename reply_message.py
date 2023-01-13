import assembler_message


def message(c_id, call, Sheet):
    if 'NOK' not in c_id['checklist']['log']:
        text = assembler_message.assembler_good(c_id, Sheet)
