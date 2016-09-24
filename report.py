# coding=utf-8
import xlrd
"""
+открываем файл
Тип Имя Кошелек Категория Сумма Валюта Дата Описание
+читаем
"""

rb = xlrd.open_workbook('c:/exportXLS.xls',formatting_info=True,encoding_override='cp1251')
# не правильное считается дата
sheet = rb.sheet_by_index(1)
lst=[sheet.row_values(rownum)for rownum in range(sheet.nrows)]
dict={}
for x in lst:
    if dict.has_key(x[3]):
        dict[x[3]] = dict[x[3]]+abs(x[4])
    else:
        dict[x[3]] = abs(x[4])

for x in sorted(dict, key=dict.__getitem__, reverse=True):
    print("%s = %s " % (x, dict[x]))