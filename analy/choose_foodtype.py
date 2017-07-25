# -*- coding : utf-8-*-
# coding:utf8
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def scrapy_type(foodtype):
    db = MySQLdb.connect("localhost","root","okgoogle","dianpingshop" ,charset='utf8')
    cursor = db.cursor()
    #cursor.execute('insert into dianpingshopx (select * from dianpingshop where foodtype = "自助餐") ;')
    #cursor.execute('insert into dianpingshopx (select * from dianpingshop where foodtype = %s' %(foodtype))
    
    sql = """insert into dianpingshopx (select * from yangzhoushop where foodtype = %s)""" %foodtype.encode("utf-8")
    cursor.execute(sql)
    print "create table sucessful!！"
    db.commit()
    db.close()



if __name__=="__main__":
    raw_input_A = raw_input("input foodtype: ")
    print "the foodtype you choose is:%s" %raw_input_A
    foodtype = str(raw_input_A)

    raw_input_A= '\'' + raw_input_A+ '\''

    scrapy_type(raw_input_A)
