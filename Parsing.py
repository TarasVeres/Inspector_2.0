# coding=utf-8
import json
import pprint

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1ClqEeSnAQhM35_dLuMKJ2Z65cposArk4HwGsf1FAGRw'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

Sheet = dict()


def func_access_id():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Access_id!A1:B100',
                                            majorDimension='ROWS').execute()
    Sheet['Access_id'] = {}
    for i in _['values']:
        try:
            Sheet['Access_id'][int(i[0])] = i[1]
        except IndexError:
            pass
    return Sheet


def func_kl_r_m():
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='KL_R_M!A1:A100',
                                            majorDimension='ROWS').execute()
    Sheet['KL_R_M'] = []
    for i in _['values']:
        Sheet['KL_R_M'] += i
    return Sheet


def func_type_district():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Type Distric!A1:Z100',
                                            majorDimension='ROWS').execute()
    for i in _['values']:
        Sheet[i[0]] = i[1:]
    return Sheet

def func_location():
    global Sheet, Location, floor, District, KL, RM, Project
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Location!A1:Z500',
                                            majorDimension='ROWS').execute()
    Sheet['Location'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                Location = i[0]
                Sheet['Location'][Location] = {}
            if i[1] != '':
                floor = i[1]
                Sheet['Location'][Location][floor] = {}
            if i[2] != '':
                District = i[2]
                Sheet['Location'][Location][floor][District] = [] if i[3] == i[-1] else {}
            if (i[3] != '') and (i[3] == i[-1]):
                KL = i[3]
                Sheet['Location'][Location][floor][District] += [KL]
            if (i[3] != '') and (i[3] != i[-1]):
                KL = i[3]
                Sheet['Location'][Location][floor][District][KL] = [] if i[4] == i[-1] else {}
            if (i[4] != '') and (i[4] == i[-1]):
                RM = i[4]
                Sheet['Location'][Location][floor][District][KL] += [RM]
            if (i[4] != '') and (i[4] != i[-1]):
                RM = i[4]
                Sheet['Location'][Location][floor][District][KL][RM] = [] if i[5] == i[-1] else {}
            if (i[5] != '') and (i[5] == i[-1]):
                Project = i[5]
                Sheet['Location'][Location][floor][District][KL][RM] += [Project]
        except (IndexError, KeyError):
            pass
    return Sheet


def func_device():
    global Sheet, Type_Device, Device, Project
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Device!A1:Z500',
                                            majorDimension='ROWS').execute()
    Sheet['Device'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                Type_Device = i[0]
                Sheet['Device'][Type_Device] = [] if i[1] == i[-1] else {}
            if (i[1] != '') and (i[1] == i[-1]):
                Device = i[1]
                Sheet['Device'][Type_Device] += [Device]
            if (i[1] != '') and (i[1] != i[-1]):
                Device = i[1]
                Sheet['Device'][Type_Device][Device] = [] if i[2] == i[-1] else {}
            if (i[2] != '') and (i[2] == i[-1]):
                Project = i[2]
                Sheet['Device'][Type_Device][Device] += [Project]
        except (IndexError, KeyError):
            pass
    return Sheet

def func_kit():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Kit!A1:A100',
                                            majorDimension='ROWS').execute()
    Sheet['kit'] = []
    for i in _['values']:
        Sheet['kit'] += i
    return Sheet

def func_reported_sp():
    global Sheet, Location, District, SP
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Reported SP!A1:Z500',
                                            majorDimension='ROWS').execute()
    Sheet['SP'] = {}
    try:
        for i in _['values']:
            if i[0] != '':
                Location = i[0]
                Sheet['SP'][Location] = {}
            if i[1] != '':
                District = i[1]
                Sheet['SP'][Location][District] = []
            if (i[2] != '') and (i[2] == i[-1]):
                sp = i[2]
                Sheet['SP'][Location][District] += [sp]
    except (IndexError, KeyError):
        pass
    return Sheet

def func_group():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Group discrepancy!A1:A100',
                                            majorDimension='ROWS').execute()
    Sheet['Group'] = []
    for i in _['values']:
        Sheet['Group'] += i
    return Sheet

def func_checklist():
    global Sheet, District, Group_defect, Request
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Checklist!A1:E300',
                                            majorDimension='ROWS').execute()
    Sheet['CheckList'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                District = i[0]
                Sheet['CheckList'][District] = {}
            if i[1] != '':
                Group_defect = i[1]
                Sheet['CheckList'][District][Group_defect] = {}
            if i[2] != '':
                Request = i[2]
                Sheet['CheckList'][District][Group_defect][Request] = {}
            if (i[3] != '') and (i[3] == i[-1]):
                Sheet['CheckList'][District][Group_defect][Request]['time_inspection'] = int(i[3])
                Sheet['CheckList'][District][Group_defect][Request]['rating'] = int(i[4])
        except (IndexError, KeyError):
            pass
    return Sheet

def beginning():
    func_access_id()
    func_kl_r_m()
    func_type_district()
    func_location()
    func_device()
    func_kit()
    func_reported_sp()
    func_group()
    func_checklist()
    with open("data_file.json", "w") as write_file:
        json.dump(Sheet, write_file, ensure_ascii=False, skipkeys=False, indent=4)
    return Sheet

beginning()