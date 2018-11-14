# -*- coding: utf-8 -*-
import collections
import money
import sqlite3

con = sqlite3.connect('test.db')
cur = con.cursor()


def report_by_all_month():
    """
    отчет за год
    :return:
    """
    current_year = money.get_current_year()
    m = collections.OrderedDict(sorted(money.months.items(), key=lambda t: t[1]))
    for month in m.values():
        first, last = money.last_first_day(current_year, month)
        result = cur.execute("SELECT sum(sum) from transactions t where t.date between '{}' and '{}'".format(first, last)).fetchall()
        if result[0][0] is not None: print first, round(result[0][0], 2)


def report_by_month(year, month, type):
    """
    отчет за месяц по родительским категориям
    """
    # прикол, если type не передавать из sys.argv - то тут приходит int
    # если передать - строка
    first, last = money.last_first_day(year, money.get_month_day(month))
    if type == '1':
        result = cur.execute("SELECT sum(sum), c.id from transactions t join category c on t.category_id = c.id "
                             "where t.date between  ? and ? group by t.category_id", (first, last,)).fetchall()
    else:
        result = cur.execute("SELECT sum(sum), c.id from transactions t join category c on t.category_id = c.id "
                             "where t.date between  ? and ? group by c.parent_id ",
                             (first, last,)).fetchall()
    for i in sorted(result, key=lambda t: t[0], reverse=True):
        print(u"{:>25} | {:<25} ".format(money.get_category(i[1]), i[0]))



def report_by_year(i):
    return cur.execute("SELECT sum(sum) from transactions where date between  ? and ? and source=0", (i, i,).fetchall())


def get_report_by_categorie(category, month):
    """
    строим отчет по родительской категории и месяцу, по дефолту текущий
    :param category:
    :param month:
    :return:
    """
    reporting_month = money.months[month] or money.get_current_month()
    first, last = money.last_first_day(dt.datetime.now().year, reporting_month)
    print(cur.execute(("SELECT sum(sum),category_id from transactions"
                          " where category_id = {} and date between '{}' and '{}';").format(category, first, last)).fetchall())


