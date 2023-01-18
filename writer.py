# coding=utf-8
import time
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

import matrix

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1ClqEeSnAQhM35_dLuMKJ2Z65cposArk4HwGsf1FAGRw'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

number_false = 1
number_result = 1

def update_number_false():
    global number_false
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Print_false!A1:A21000', majorDimension='COLUMNS').execute()
    number_false = int(_['values'][-1][-1]) if _['values'][-1][-1] != '№' else 1
    return number_false

def update_number_result():
    global number_result
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Print_result!A1:A21000', majorDimension='COLUMNS').execute()
    number_result = int(_['values'][-1][-1]) if _['values'][-1][-1] != '№' else 1
    return number_result

def writer_false(c_id, data):
    global number_false
    value = [[''] for i in range(12)]
    value[0] = [str(update_number_false() + 1)]
    value[1] = [time.strftime("%d.%m.%Y", time.localtime())]
    value[2] = [c_id['shift']]
    value[3] = [c_id['location']]
    value[4] = [c_id['district']]
    if  ("Без роб місця" not in c_id['room']) and ("Без р.м." not in c_id['room']):
        value[5] = [c_id['room']]
    else:
        value[5] = ['']
    if 'project' in c_id:
        value[6] = [c_id['project']]
    else:
        if 'Без девайсу'not in c_id['device']:
            value[6] = [c_id['device']]
        else:
            pass
    value[7] = [c_id['sp']]
    value[8] = [data['output_defect_message']]
    value[9] = [data['district']]
    value[10] = [data['text']]
    value[11] = [c_id['inspector']]
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Print_false!A{number_false + 1}:L21000',
                 "majorDimension": "COLUMNS",
                 "values": value}
            ]
        }
    ).execute()

def writer_result(c_id):
    global number_result
    value = [[''] for i in range(9)]
    value[0] = [str(update_number_result() + 1)]
    value[1] = [time.strftime("%d.%m.%Y", time.localtime())]
    value[2] = [c_id['shift']]
    value[3] = [c_id['location']]
    value[4] = [c_id['district']]
    value[5] = [c_id['sp']]
    value[6] = [f'{matrix.count_result(c_id)}%']
    value[7] = [c_id['inspector']]
    value[8] = [matrix.count_time_inspection(c_id)]
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Print_result!A{number_result + 1}:I21000',
                 "majorDimension": "COLUMNS",
                 "values": value}
            ]
        }
    ).execute()
