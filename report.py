# coding=utf-8
import xlrd
"""
+открываем файл
Тип Имя Кошелек Категория Сумма Валюта Дата Описание
+читаем
"""

rb = xlrd.open_workbook('c:/exportXLS.xls',formatting_info=True)
sheet = rb.sheet_by_index(0)
lst=[]
for rownum in range(sheet.nrows):
    row = sheet.row_values(rownum)
    lst.append(row)
for x in lst:
    pass
