# coding=utf-8
import xlrd
rb = xlrd.open_workbook('c:/exportXLS.xls',formatting_info=True,encoding_override='cp1251')
# не правильно считается дата
sheet = rb.sheet_by_index(1)
lst=[sheet.row_values(rownum)for rownum in range(sheet.nrows)]
dict={}
for x in lst:
    if dict.has_key(x[3]):
        dict[x[3]] = dict[x[3]]+abs(x[4])
    else:
        dict[x[3]] = abs(x[4])

for x in sorted(dict, key=dict.__getitem__, reverse=True):
    if x != u'': print("%s = %s " % (x, dict[x]))