# -*- coding: utf-8 -*-
import argparse
import json
import sqlite3
from my_transactions import Transactions
from my_category import Category
from datetime import datetime as dt
import collections

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


def mysql_fill():
    cur.execute('DROP TABLE IF EXISTS category')
    cur.execute('CREATE TABLE category (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, available INTEGER, '
                'order_id INTEGER, parent_id INTEGER)')
    cur.execute('DROP TABLE IF EXISTS transactions')
    cur.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, '
                'category_id INTEGER, date DATETIME, sum INTEGER, account_id INTEGER, description VARCHAR(100),'
                ' source INTEGER, available INTEGER)')
    con.commit()
    file = open("/Users/i.kudryashov/Desktop/financePM.data", "r").read()
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
            trn.date = dt.fromtimestamp(int(transaction['date']) / 1000)
            cur.execute('INSERT INTO transactions (id,name,type,category_id,date,sum,account_id,description,'
                    'source,available) values'
                    '(?,?,?,?,?,?,?,?,?,?)', trn.return_list(),)
            con.commit()
    cur.close()
    print('Done!')


def get_category(id):
    if id != 0: result = cur.execute('select name from category where id = ?', (id,)).fetchall()
    else: result = [['None']]
    return result[0][0]


def last_first_day(year, month):
    # тут костыль, потому что between почему то справа ограничивает срого ( <)
    # придумать что то с этим
    first = year + '-' + month[1] + '-' + month[0]
    last = year + '-' + '0' + str(int(month[1])+1) + '-' + month[0]
    return first, last


def report_by_all_month():
    current_year = '2017'
    m = collections.OrderedDict(sorted(months.items(), key=lambda t:[1]))
    for month in m.values():
        first, last = last_first_day(current_year, month)
        result = cur.execute("SELECT sum(sum) from transactions t join category c on t.category_id = c.id  "
                                 "where t.date between ? and ?", (first, last,)).fetchall()
        # print(1,2) выведет на печать (1,2) и терминал не прожует русские буквы выведет их аски код
        # а если запускать через питон3 - то ок
        if result[0][0] is not None: print(first, round(result[0][0], 2))


def report_by_month(year, month, type):
    # прикол, если type не передавать из sys.argv - то тут приходит int
    # если передать - строка
    first, last = last_first_day(year, get_month_day(month))
    if type == '1':
        result = cur.execute("SELECT sum(sum), c.name, c.id from transactions t join category c on t.category_id = c.id "
                             "where t.date between  ? and ? group by t.category_id "
                             "order by sum(sum) desc", (first, last,)).fetchall()
        for i in result:
            print(u"{} {} {}".format(i[2], i[1], i[0]))
    else:
        result = cur.execute("SELECT sum(sum), c.parent_id, c.id from transactions t join category c on t.category_id = c.id "
                             "where t.date between  ? and ? group by c.parent_id "
                             "order by sum(sum) desc",
                             (first, last,)).fetchall()
        for i in result:
            print(u"{} {} {}".format(i[2], get_category(i[1]), i[0]))


def report_by_year(i):
    return cur.execute("SELECT sum(sum) from transactions where date between  ? and ? and source=0", (i, i,).fetchall())


def get_month_day(month):
    return months[month]


def get_current_month():
    return dt.today()


def get_report_by_categorie(category, month=get_current_month()):
    """
    строим отчет по родительской категории и месяцу, по дефолту текущий
    :param category:
    :param month:
    :return:
    """
    result = cur.execute(("SELECT sum(sum) from transactions where category_id = {} and date between {} and {};").format(category))
    for i in result:
        print(i)


    """
    написать еще очет за месяц по категориям
    +отчет по родительским категориям
    отчет по доходам

    сейчас вижу все траты, сделать так чтобы можно было исключать категории
    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('--all', action='store_true', help='Report by all month')
    parser.add_argument('-m', '--month', help='Report by one month. Key works only witn --year')
    parser.add_argument('-y', '--year')
    parser.add_argument('-c', '--category', action='store')
    parser.add_argument('-t', '--type', action='store', help='1: full category, 0: only parent, default=0', default=0)
    parser.add_argument('-f', '--fill', action='store_true')
    args = parser.parse_args()
    if args.all:
        report_by_all_month()
    elif args.month or args.year:
        if args.year is None:
            args.year = '2017'
        report_by_month(args.year, args.month, args.type)
    elif args.category:
        get_report_by_categorie(args.category, args.month)
    elif args.fill:
        mysql_fill()



