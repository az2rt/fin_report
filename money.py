import json
import sqlite3
from datetime import datetime as dt
year = ['2015','2016','2017']
con = sqlite3.connect('test7.db')
cur = con.cursor()
months={
    'january':  '01,01,31',
    'february': '02,01,28',
    'march':    '03,01,30',
    'april':    '04,01,31',
    'may':      '05,01,30',
    'june':     '06,01,31',
    'july':     '07,01,30',
    'august':   '08,01,31',
    'september':'09,01,30',
    'october':  '10,01,31',
    'november': '11,01,30',
    'december': '12,01,31'
}


def mysql_fill():
    cur.execute('DROP TABLE IF EXISTS category ')
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
        cur.execute('INSERT INTO category (id,name,type,available,order_id,parent_id) values (?,?,?,?,?,?)',
                    tuple(category.values(),))
        con.commit()

    for transaction in json_row['transactions']:
        transaction['date'] = dt.fromtimestamp(int(transaction['date']) / 1000)
        cur.execute('INSERT INTO transactions (id,name,type,category_id,date,sum,account_id,description,'
                    'source,available) values'
                    '(?,?,?,?,?,?,?,?,?,?)', tuple(transaction.values(),))
        con.commit()
    cur.close()


def get_category():
    return cur.execute('select * from category')


def report_by_all_month():
    for current_year in year:
        for month, number in months.items():
            day_month = number.split(",")
            first = current_year+'-'+day_month[0]+'-'+day_month[1]
            last = current_year+'-'+day_month[0]+'-'+day_month[2]
            result = cur.execute("SELECT sum(sum) from transactions t join category c on t.category_id = c.id  "
                                 "where t.date between ? and ? and t.type = 2 ", (first, last,)).fetchall()
            if result[0][0] is not None: print(current_year, month, round(result[0][0], 2))
    con.close()

"""
написать еще очет за месяц по категориям
отчет по родительским категориям
отчет по доходам
прикрутить графики
сейчас вижу все траты, сделать так чтобы можно было исключать категории
"""
report_by_all_month()

