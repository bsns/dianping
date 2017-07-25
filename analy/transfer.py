# coding:utf8
import sys
import xlwt
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf8')

def export_mysqltable_xls(choice):
    conn = MySQLdb.connect('localhost','root','okgoogle','dianpingshop',charset='utf8')
    cursor = conn.cursor()
    global tablename
    if choice == 1:
        count = cursor.execute('select * from dianpingshop')
        tablename = 'dianpingshop'
    elif choice == 2:
        count = cursor.execute('select * from pagecomment')
    elif choice == 3:
        count = cursor.execute('select * from user')
    elif choice == 4:
        count = cursor.execute('select * from user_shop')
    else:
        count = cursor.execute('select * from yangzhoushop')

    print count

    cursor.scroll(0,mode='absolute')
    results = cursor.fetchall()

    fields = cursor.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('content',cell_overwrite_ok=True)

    for field in range(0,len(fields)):
        sheet.write(0,field,fields[field][0])

    row = 1
    col = 0
    for row in range(1,len(results)+1):
        for col in range(0,len(fields)):
            sheet.write(row,col,u'%s'%results[row-1][col])
    if choice == 1:
        workbook.save(r'./dianpingshop.xls')
    elif choice ==2:
        workbook.save(r'./pagecomment.xls')
    elif choice ==3:
        workbook.save(r'./user.xls')
    elif choice == 4:
        workbook.save(r'./user_listshop.xls')
    else:
        workbook.save(r'./yangzhoushop.xls')

if __name__ == '__main__':
    print "Enter 1 to export dianpingshop"
    print "Enter 2 to export pagecomment"
    print "Enter 3 to export user"
    print "Enter 4 to export user_listshop"
    print "Enter 5 to export yangzhoushop"
    print "Or enter 6 to export all tables"
    print "Enter your choice:"
    choice = int(raw_input("Input your choice:"))
    if choice == 1:
        export_mysqltable_xls(1)
    elif choice == 2:
        export_mysqltable_xls(2)
    elif choice == 3:
        export_mysqltable_xls(3)
    elif choice == 4:
        export_mysqltable_xls(4)
    elif choice == 5:
        export_mysqltable_xls(5)
    elif choice ==6 :
        export_mysqltable_xls(1)
        export_mysqltable_xls(2)
        export_mysqltable_xls(3)
        export_mysqltable_xls(4)
        export_mysqltable_xls(5)

    else:
        print "Error!"
