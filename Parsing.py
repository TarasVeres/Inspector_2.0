# coding=utf-8
import json

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '12gvu_yxTqLfIPNo-T8unIhaz4AoAevydHy4EM1vb0Ig'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

Sheet = dict()


def func_Access_id():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Access_id_lang!A1:D100', majorDimension='ROWS').execute()
    Sheet['Access_id'] = {}
    for i in _['values']:
        try:
            Sheet['Access_id'][int(i[1])] = i[2]
        except IndexError:
            pass
    return Sheet


def func_KL_R_M():
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='KL_R_M!A1:A100', majorDimension='ROWS').execute()
    Sheet['KL_R_M'] = []
    for i in _['values']:
        Sheet['KL_R_M'] += i
    return Sheet


def func_Type_distric():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Type distric!A1:Z100', majorDimension='ROWS').execute()
    for i in _['values']:
        Sheet[i[0]] = i[1:]
    return Sheet


def func_Location():
    global Sheet, Location, Floor, Distric, KL, RM, Project
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Location!A1:Z500', majorDimension='ROWS').execute()
    Sheet['Location'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                Location = i[0]
                Sheet['Location'][Location] = {}
            if i[1] != '':
                Floor = i[1]
                Sheet['Location'][Location][Floor] = {}
            if i[2] != '':
                Distric = i[2]
                Sheet['Location'][Location][Floor][Distric] = [] if i[3] == i[-1] else {}
            if (i[3] != '') and (i[3] == i[-1]):
                KL = i[3]
                Sheet['Location'][Location][Floor][Distric] += [KL]
            if (i[3] != '') and (i[3] != i[-1]):
                KL = i[3]
                Sheet['Location'][Location][Floor][Distric][KL] = [] if i[4] == i[-1] else {}
            if (i[4] != '') and (i[4] == i[-1]):
                RM = i[4]
                Sheet['Location'][Location][Floor][Distric][KL] += [RM]
            if (i[4] != '') and (i[4] != i[-1]):
                RM = i[4]
                Sheet['Location'][Location][Floor][Distric][KL][RM] = [] if i[5] == i[-1] else {}
            if (i[5] != '') and (i[5] == i[-1]):
                Project = i[5]
                Sheet['Location'][Location][Floor][Distric][KL][RM] += [Project]
        except (IndexError, KeyError):
            pass
    return Sheet


def func_Device():
    global Sheet, Type, Device, Project
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Device!A1:Z500', majorDimension='ROWS').execute()
    Sheet['Device'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                Type = i[0]
                Sheet['Device'][Type] = [] if i[1] == i[-1] else {}
            if (i[1] != '') and (i[1] == i[-1]):
                Device = i[1]
                Sheet['Device'][Type] += [Device]
            if (i[1] != '') and (i[1] != i[-1]):
                Device = i[1]
                Sheet['Device'][Type][Device] = [] if i[2] == i[-1] else {}
            if (i[2] != '') and (i[2] == i[-1]):
                Project = i[2]
                Sheet['Device'][Type][Device] += [Project]
        except (IndexError, KeyError):
            pass
    return Sheet

def func_Kit():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Kit!A1:A100', majorDimension='ROWS').execute()
    Sheet['Kit'] = []
    for i in _['values']:
        Sheet['Kit'] += i
    return Sheet

def func_Reported_SP():
    global Sheet, Location, Distric, SP
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Reported SP!A1:Z500', majorDimension='ROWS').execute()
    Sheet['SP'] = {}
    try:
        for i in _['values']:
            if i[0] != '':
                Location = i[0]
                Sheet['SP'][Location] = {}
            if i[1] != '':
                Distric = i[1]
                Sheet['SP'][Location][Distric] = []
            if (i[2] != '') and (i[2] == i[-1]):
                SP = i[2]
                Sheet['SP'][Location][Distric] += [SP]
    except (IndexError, KeyError):
        pass
    return Sheet

def func_Group():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Group discrepancy!A1:A100', majorDimension='ROWS').execute()
    Sheet['Group'] = []
    for i in _['values']:
        Sheet['Group'] += i
    return Sheet

def func_Checklist():
    global Sheet, District, Group_defect, Request, Time
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Checklist!A1:E300', majorDimension='ROWS').execute()
    Sheet['Checklist'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                District = i[0]
                Sheet['Checkist'][District] = {}
            if i[1] != '':
                Group_defect = i[1]
                Sheet['Checklist'][District][Group_defect] = {}
            if i[2] != '':
                Request = i[2]
                Sheet['Checklist'][District][Group_defect][Request] = [] if i[3] == i[-1] else {}
            if (i[3] != '') and (i[3] == i[-1]):
                Time = i[3]
                Sheet['Checklist'][District][Group_defect][Request] += [Time]
            if (i[3] != '') and (i[3] != i[-1]):
                Time = i[3]
                Sheet['Checklist'][District][Group_defect][Request][Time] = [] if i[4] == i[-1] else {}
            if (i[4] != '') and (i[4] == i[-1]):
                Rating = i[4]
                Sheet['Checklist'][District][Group_defect][Request][Time] += [Rating]
        except (IndexError, KeyError):
            pass
    return Sheet


def beginning():
    func_Access_id()
    func_KL_R_M()
    func_Type_distric()
    func_Location()
    func_Device()
    func_Kit()
    func_Reported_SP()
    func_Group()
    func_Checklist()
    with open("data_file.json", "w") as write_file:
        json.dump(Sheet, write_file, ensure_ascii=False, skipkeys=False, indent=4)
    return

beginning()