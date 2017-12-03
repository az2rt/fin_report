# -*- coding: utf-8 -*-
import argparse
import json
import sqlite3
from Transactions import Transactions
from Category import Category
import Reports
import datetime as dt

con = sqlite3.connect('test.db')
cur = con.cursor()
months = {
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

months_words = {
    1:'january',
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


def mysql_fill():
    cur.execute('DROP TABLE IF EXISTS category')
    cur.execute('CREATE TABLE category (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, available INTEGER, '
                'order_id INTEGER, parent_id INTEGER)')
    cur.execute('DROP TABLE IF EXISTS transactions')
    cur.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, '
                'category_id INTEGER, date DATETIME, sum INTEGER, account_id INTEGER, description VARCHAR(100),'
                ' source INTEGER, available INTEGER)')
    con.commit()
    file = open("./financePM.data", "r").read()
    json_row = json.loads(file)
    for category in json_row['categories']:
        cat = Category(category)
        cur.execute('INSERT INTO category (id,name,type,available,order_id,parent_id) values (?,?,?,?,?,?)',
                    cat.return_list(),)
        con.commit()

    for transaction in json_row['transactions']:
        trn = Transactions(transaction)
        # проверка на расходы
        if trn.source == 0 and trn.type == 2:
            trn.date = dt.datetime.fromtimestamp(int(transaction['date']) / 1000)
            cur.execute('INSERT INTO transactions (id,name,type,category_id,date,sum,account_id,description,'
                    'source,available) values (?,?,?,?,?,?,?,?,?,?)', trn.return_list(),)
            con.commit()
    cur.close()
    print('Done!')


def get_category(id):
    if id: result = cur.execute('select name from category where id = ?', (id,)).fetchall()
    else: result = [['None']]
    return result[0][0]


def last_first_day(year, month):
    first = dt.date(int(year),int(month[1]),int(month[0])).isoformat()
    last = dt.date(int(year), int(month[1]),int(month[2])).isoformat()
    return first, last


def get_month_day(month):
    """
    получить цифровое представление месяцв
    """
    return months[month]


def get_current_year():
    return dt.datetime.now().year


def get_current_month():
    return months[months_words[dt.datetime.now().month]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('--all', action='store_true', help='Report by all month')
    parser.add_argument('-rm', '--report_by_month', help='Report by one month. Key works only witn --year')
    parser.add_argument('-y', '--year')
    parser.add_argument('--show', action='store_true')
    parser.add_argument('-c', '--category', action='store')
    parser.add_argument('-m', '--month', action='store')
    parser.add_argument('-t', '--type', action='store', help='1: full category, 0: only parent, default=0', default=0)
    parser.add_argument('-f', '--fill', action='store_true')
    args = parser.parse_args()
    if args.all:
        Reports.report_by_all_month()
    elif args.report_by_month:
        if args.year is None:
            args.year = str(dt.datetime.now().year)
        Reports.report_by_month(args.year, args.report_by_month, args.type)
    elif args.category:
        Reports.get_report_by_categorie(args.category, args.month)
    elif args.show:
        for i in (cur.execute("select parent_id,id,name from category order by parent_id").fetchall()):
            print(u'{} {} {}'.format(i[0], i[1], i[2]))
    elif args.fill:
        mysql_fill()



