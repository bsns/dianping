# coding:utf8
import numpy as np
import pylab as pl
import MySQLdb
import os

def seek_num(key, content, pr_value, af_value):
    db = MySQLdb.connect("localhost","root","okgoogle","dianpingshop" )
    cursor = db.cursor()
    cursor.execute('select %s from yangzhoushop where %s between %s and %s' %(key,content,pr_value,af_value))
    results = cursor.fetchall()
    tempInt =0
    for i in results:
	try:
		tempInt=int(i[0])
		print tempInt
	except: pass
    db.close()
    return tempInt



def show_price():

    x = []
    y = []
    z = []
    a = []
    for numx in range(10, 200, 10):
        x.append(numx)
        valuesy = seek_num('avg(reviewnum)', 'avgcost', numx-10, numx)
        y.append(valuesy)
        values = seek_num('count(*)', 'avgcost', numx-10, numx)
        z.append(values)
        valuesa = seek_num('avg(taste)', 'avgcost', numx-10, numx)
        a.append(valuesa*10)
    print x

    print z
    #pl.plot(x, y)# use pylab to plot x and y
    #pl.plot(x, y, z, '-or')
    pl.plot(x, y, '-r')
    pl.plot(x, z)
    pl.plot(x, a)
    pl.xlabel(u'价格')
    pl.ylabel(u'人数')
    pl.title(u'扬州的平均消费')
    pl.show()# show the plot on the screen

if __name__ == '__main__':

    show_price()
