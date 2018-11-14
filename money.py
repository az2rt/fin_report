# -*- coding: utf-8 -*-
import argparse
import json
import sqlite3
import pprint
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

from models.transactions import Transactions
from models.category import Category
from utils.utils import MONTHS, MONTHS_WORDS


con = sqlite3.connect('./tmp/test.db')
cur = con.cursor()


def prepare_db(func):
    def wrapped():
        cur.execute('DROP TABLE IF EXISTS category')
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


@prepare_db
def mysql_fill():
    with open('./tmp/financePM.data', 'r') as f:
        json_row = json.loads(f.read())

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
                    'source,available) values (?,?,?,?,?,?,?,?,?,?)', trn.return_list(),)
            con.commit()
    print('Done!')


def get_category(category_id):
    if id:
        result = cur.execute('select name from category where id = ?', (category_id,)).fetchall()
    else:
        result = [['None']]
    return result[0][0]


def last_first_day(year, month):

    if type(year) is int:
        year = str(year)
    first = year + '-' + month[1] + '-' + month[0]
    last = year + '-' + month[1] + '-' + month[2]
    return first, last


def get_first_transactions():
    result = cur.execute('select date from transactions order by date limit 1')
    return result.fetchall()[0][0]


def get_last_transactions():
    result = cur.execute('select date from transactions order by date desc limit 1')
    return result.fetchall()[0][0]


def date_from_str_to_datetime(date):
    return dt.strptime(date[:4], '%Y')


def plus_one_year(old_date):
    return old_date + relativedelta(years=1)


def report_by_all_month():
    """
    report by per year on all categories
    """
    first_transaction = get_first_transactions()
    last_transaction = get_last_transactions()
    current_year = date_from_str_to_datetime(first_transaction)

    while current_year <= date_from_str_to_datetime(last_transaction):
        result = cur.execute(
            "SELECT sum(sum) from transactions where date between '{}' and '{}'".format(
                current_year, plus_one_year(current_year).isoformat()
            )).fetchall()
        if result:
            print('Year: {} summary: {}'.format(current_year.year, result[0][0]))
        current_year = current_year + relativedelta(years=1)


def report_by_month(year, month, type_report):

    first, last = last_first_day(year, MONTHS[month])

    if type_report:
        result = cur.execute("SELECT sum(sum), c.id from transactions t join category c on t.category_id = c.id "
                             "where t.date between  ? and ? group by t.category_id", (first, last,)).fetchall()
    else:
        result = cur.execute("SELECT sum(sum), c.id from transactions t join category c on t.category_id = c.id "
                             "where t.date between  ? and ? group by c.parent_id ",
                             (first, last,)).fetchall()
    if result == []:
        print('Dont find any transactions by this date: {} {}.'.format(month, year))
    for i in sorted(result, key=lambda t: t[0], reverse=True):
        print(u"{:>25} {}".format(get_category(i[1]), i[0]))


def get_current_month():
    return MONTHS[MONTHS_WORDS[dt.now().month]]


def get_report_by_categorie(category, month=get_current_month()):
    """
    строим отчет по родительской категории и месяцу, по дефолту текущий
    """
    first, last = last_first_day(dt.now().year, month)
    result = cur.execute(
        (
            "SELECT sum(sum) from transactions where category_id = {} and date between {} and {};").format(
            category,
            first,
            last
        ))
    for i in result:
        pprint.pprint(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('--all', action='store_true', help='Report by all month')
    parser.add_argument('-rm', '--report_by_month', help='Report by one month. Key works only witn --year')
    parser.add_argument('-y', '--year')
    parser.add_argument('--show', action='store_true')
    parser.add_argument('-c', '--category', action='store')
    parser.add_argument('-t', '--type', action='store', help='1: full category, 0: only parent, default=0', default=0)
    parser.add_argument('-f', '--fill', action='store_true')
    args = parser.parse_args()
    if args.all:
        report_by_all_month()
    elif args.report_by_month:
        if args.year is None:
            args.year = dt.now().year
        report_by_month(args.year, args.report_by_month, args.type)
    elif args.category:
        get_report_by_categorie(args.category)
    elif args.show:
        test = Category()
    elif args.fill:
        mysql_fill()
