# coding=utf-8
import json

from Parsing import beginning


def update_sheet():
    beginning()
    with open('data_file.json', 'r') as read_file:
        sheet = json.load(read_file)
    return sheet


def open_json():
    with open('data_file.json', 'r') as read_file:
        sheet = json.load(read_file)
    return sheet
