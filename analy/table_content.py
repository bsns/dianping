import xlwt
import xlrd
from xlutils.copy import copy
import MySQLdb.cursors
import xlsxwriter
from xlrd import open_workbook
from xlutils.copy import copy


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
    conn = MySQLdb.connect(user='root', passwd='okgoogle', db='dianpingshop', host='localhost', charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    i = 1
    file = xlwt.Workbook()
    table = file.add_sheet('table1',cell_overwrite_ok=True)
    for x in range(1, 194):
        for y in range(1, 19):
            _id = int(excel_read('/Users/bsns/Workspaces/analy/first.xls','table1',0,y))
            #print '_id='
            #print _id

            shop_id = int(excel_read('/Users/bsns/Workspaces/analy/first.xls','table1',x,0))
            #print shop_id
            cursor.execute('select shoplevel from user_shop where _id = %s and shopurl = %s ;' % (_id, shop_id))
            results = cursor.fetchall()
            insert_value = 0
            for i in results:
                #tempInt=int(i[0])
                #print tempInt
                print i[0]
                insert_value = i[0]
                #table.write(x,y,i[0])
            #excel_create('table1', i[0], x, y)
            if insert_value != 0:
                rb = open_workbook('first.xls')
                wb = copy(rb)
                sheet = wb.get_sheet(0)
                sheet.write(x, y, insert_value)
                wb.save('first.xls')
            else:
                print "null"
