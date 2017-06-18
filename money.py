# -*- coding: utf-8 -*-
import argparse
import json
import sqlite3
import Category, Transactions
from datetime import datetime as dt

year = ['2015', '2016', '2017']
con = sqlite3.connect('test.db')
cur = con.cursor()
months={
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

class Category:

    def __init__(self, query):
        self.name = query['name']
        self.id = query['id']
        self.type = query['type']
        self.available = query['available']
        self.order_id = query['orderId']
        self.parent_id = query['parentId']

    def return_list(self):
        return (self.id,self.name,self.type,self.available,self.order_id,self.parent_id)

class Transactions:

    def __init__(self, query):
        self.name = query['name']
        self.id = query['id']
        self.type = query['type']
        self.category_id = query['categoryId']
        self.date = query['date']
        self.sum = query['sum']
        self.account = query['accountId']
        self.desc = query['description']
        self.source = query['source']
        self.available = query['available']

    def return_list(self):
        return (self.id, self.name, self.type, self.category_id, self.date, self.sum, self.account, self.desc,
                self.source, self.available)


def mysql_fill():
    cur.execute('DROP TABLE IF EXISTS category')
    cur.execute('CREATE TABLE category (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, available INTEGER, '
                'order_id INTEGER, parent_id INTEGER)')
    cur.execute('DROP TABLE IF EXISTS transactions')
    cur.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY, name VARCHAR(100), type INTEGER, '
                'category_id INTEGER, date DATETIME, sum INTEGER, account_id INTEGER, description VARCHAR(100),'
                ' source INTEGER, available INTEGER)')
    con.commit()
    file = open("/Users/i.kudryashov/Documents/financePM.data", "r").read()
    json_row = json.loads(file)
    for category in json_row['categories']:
        cat = Category(category)
        cur.execute('INSERT INTO category (id,name,type,available,order_id,parent_id) values (?,?,?,?,?,?)',
                    cat.return_list(),)
        con.commit()

 # здесь кажется класс не нужен, можно функцией

    for transaction in json_row['transactions']:
        trn = Transactions(transaction)
# а здесь можно проверить на type = 2 и source = 0, чтоб в транзакции попадали только траты
        trn.date = dt.fromtimestamp(int(transaction['date']) / 1000)
        cur.execute('INSERT INTO transactions (id,name,type,category_id,date,sum,account_id,description,'
                    'source,available) values'
                    '(?,?,?,?,?,?,?,?,?,?)', trn.return_list(),)
        con.commit()
    cur.close()


def mysql_select():
    """
    общая функция для запросов
    :return:
    """
    pass


def get_category():
    return cur.execute('select * from category')

# тут костыль, потому что between почему справа ограничивает срого ( <)
# придумать что то с этим
def last_first_day(year, month):
    first = year + '-' + month[1] + '-' + month[0]
    last = year + '-' + '0' + str(int(month[1])+1) + '-' + month[0]
    return first, last


def report_by_all_month():
    current_year = '2017'
    for month in months.values():
        first, last = last_first_day(current_year, month)
        result = cur.execute("SELECT sum(sum) from transactions t join category c on t.category_id = c.id  "
                                 "where t.date between ? and ? and t.type = 2 and source = 0", (first, last,)).fetchall()
        if result[0][0] is not None: print(first, round(result[0][0], 2))

# print(1,2) выведет на печать (1,2) и терминал если русские буквы выведет их аски код
def report_by_month(year,month):
    first, last = last_first_day(year, get_month_day(month))
    result = cur.execute("SELECT c.name, sum(sum) from transactions t join category c on t.category_id = c.id "
                         "where t.date between  ? and ? and t.source = 0 and t.type = 2 group by t.category_id "
                         "order by sum(sum) desc",
                         (first, last,)).fetchall()
    #import pdb; pdb.set_trace()
    for i in result:

        print i[0], i[1]

def report_by_year(year):
    return cur.execute("SELECT sum(sum) from transactions where date between  ? and ? and source=", (year, year,).fetchall())

def report_by_income():
    pass


def get_month_day(month):
    return months[month]

"""
написать еще очет за месяц по категориям
отчет по родительским категориям
отчет по доходам

сейчас вижу все траты, сделать так чтобы можно было исключать категории
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('--all', action='store_true', help='Report by all month')
    parser.add_argument('-m', '--month', help='Report by one month. Key works only witn --year')
    parser.add_argument('-y', '--year')
    parser.add_argument('--fill')
    args = parser.parse_args()
    if args.all:
        report_by_all_month()
    elif args.month and args.year:
        report_by_month(args.year, args.month)



