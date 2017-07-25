#encoding=utf-8
#coding = utf-8

import matplotlib.pyplot as plt
import time



import MySQLdb

db = MySQLdb.connect("localhost","root","okgoogle","dianpingshop",charset='utf8' )

cursor = db.cursor()
cursor.execute("select city, count(*) from user group by city order by count(*) desc;")
data = cursor.fetchall()
#print "Database version : %s " % data
for city in data:
    if city[1] > 10:
        tempcity = city[0]
        print tempcity + "%s" % (city[1])


#
db.close()
time.sleep(3)

# The slices will be ordered and plotted counter-clockwise.
labels = u'扬州', u'上海', u'南京', u'苏州', u'北京', u'其它'
sizes = [53, 23, 7, 2, 2, 13]
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'magenta', 'cyan']
explode = (0, 0.1, 0, 0, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.title(u'用户分布图')
plt.show()
