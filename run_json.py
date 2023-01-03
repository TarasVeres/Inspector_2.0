# coding=utf-8
import json
import time

from Parsing import beginning
day = 32


def checker():
    global day
    if day != time.localtime().tm_mday:
        beginning()
        with open('data_file.json', 'r') as read_file:
            Sheet = json.load(read_file)
        day = time.localtime().tm_mday
    else:
        with open('data_file.json', 'r') as read_file:
            Sheet = json.load(read_file)
    return Sheet

def update_sheet():
    beginning()
    with open('data_file.json', 'r') as read_file:
        Sheet = json.load(read_file)
    return Sheet