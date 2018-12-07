#-*- coding: utf-8 -*-
import sqlite3

MONTHS = {
    'january':  ['01','01','31'],
    'february': ['01','02','28'],
    'march':    ['01','03','31'],
    'april':    ['01','04','30'],
    'may':      ['01','05','31'],
    'june':     ['01','06','30'],
    'july':     ['01','07','31'],
    'august':   ['01','08','31'],
    'september': ['01','09','30'],
    'october':  ['01','10','31'],
    'november': ['01','11','30'],
    'december': ['01','12','31']
}

MONTHS_WORDS = {
    1: 'january',
    2: 'february',
    3: 'march',
    4: 'april',
    5: 'may',
    6: 'june',
    7: 'july',
    8: 'august',
    9: 'september',
    10: 'october',
    11: 'november',
    12: 'december'
}


def get_named_month(index_month):
    return MONTHS_WORDS[int(index_month)]


def prepare_db(func):
    con = sqlite3.connect('./tmp/test.db')
    cur = con.cursor()
    def wrapped():
        cur.execute('DROP TABLE IF EXISTS category;')
        cur.execute(
            'CREATE TABLE category (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, available INTEGER, '
            'order_id INTEGER, parent_id INTEGER)')
        cur.execute('DROP TABLE IF EXISTS transactions')
        cur.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, '
                    'category_id INTEGER, date DATETIME, sum INTEGER, account_id INTEGER, description VARCHAR(100),'
                    ' source INTEGER, available INTEGER)')
        con.commit()
        func()
        cur.close()
    return wrapped
