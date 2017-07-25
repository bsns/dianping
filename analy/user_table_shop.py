#!/usr/bin/env python
# encoding: utf-8

import xlwt
import xlrd
from xlutils.copy import copy
import MySQLdb.cursors

def excel_create(sheet, value, x, y):
     data = xlwt.Workbook()
     table = data.add_sheet(sheet)
     print x
     print y
     table.write(x,y,value)
     data.save('demo.xls')

def excel_read(doc,table,x,y):
     data = xlrd.open_workbook(doc)
     table = data.sheet_by_name(table)
     return table.cell(x,y).value


if __name__ == '__main__':
    #excel_create('',2)
    #x = excel_read('/home/bsns/Music/add/demo.xls','haha',1,4)
    #print x
    #excel_create('first', 99, 1, 1)
    conn = MySQLdb.connect(user='root', passwd='okgoogle', db='dianpingshop', host='localhost', charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM user_table_shop;')
    rows = cursor.fetchall()
    i = 1
    file = xlwt.Workbook()
    table = file.add_sheet('table1',cell_overwrite_ok=True)
    table.col(0).width = 11 * 256 + 182
    for row in rows:
        if row:
            print row[0]
            #excel_create('first', row[0], 0, i)
            table.write(0,i,row[0])
            i = i + 1
            #temp = row[0]
            #print row
        file.save('first.xls')

    cursor.close()

    cursor = conn.cursor()
    cursor.execute('SELECT shopurl FROM user_shop group by shopurl;')
    print "38================"
    rows = cursor.fetchall()
    j = 1
    #file = xlwt.Workbook()
    #table = file.add_sheet('sheet name',cell_overwrite_ok=True)
    for row in rows:
        if row:
            print row[0]
            #temp = filter(lambda ch: ch in '0123456789', row[0])
            #print temp
            #excel_create('first', row[0], 0, i)
            table.write(j,0,row[0])
            j = j + 1
            #temp = row[0]
            #print row
        file.save('first.xls')

    cursor.close()
