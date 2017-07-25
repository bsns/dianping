#coding:utf-8
from matplotlib import pyplot as plt
import numpy as np
import MySQLdb


def seek_num(key, label, af_value):
    db = MySQLdb.connect("localhost","root","okgoogle","dianpingshop" )
    cursor = db.cursor()
    cursor.execute('select %s from user where %s = %s' %(key,label,af_value))
    results = cursor.fetchall()
    tempInt =0
    for i in results:
	#try:
		tempInt=int(i[0])

    db.close()
    return tempInt


if __name__ == '__main__':
    X1 = []
    X2 = []
    vip_count = seek_num('count(*)', 'is_vip', 1)
    no_vip_count = seek_num('count(*)', 'is_vip', 0)
    vip_per = float(vip_count)/(vip_count + no_vip_count)*10
    vip_per = int(round(vip_per))
    no_vip_per = 10 - vip_per

    man_count = seek_num('count(*)', 'gender', '\'man\'')
    woman_count = seek_num('count(*)', 'gender', '\'woman\'')
    man_per = float(man_count)/(man_count + woman_count)*10
    man_per = int(round(man_per))
    woman_per = 10 - man_per
    print man_per

    X1 = np.array([no_vip_per, woman_per])
    X2 = np.array([vip_per, man_per])
    bar_labels = ['vip', u'性别:男/女']
    fig = plt.figure(figsize=(8,6))
    y_pos = np.arange(len(X1))
    y_pos = [x for x in y_pos]
    plt.yticks(y_pos, bar_labels, fontsize=10)
    plt.barh(y_pos, X1,
             align='center', alpha=0.4, color='g')
    plt.barh(y_pos, -X2,
             align='center', alpha=0.4, color='b')
    plt.xlabel(u'是/非')
    t = plt.title(u'用户基础信息')
    plt.ylim([-1,len(X1)+0.1])
    plt.xlim([-max(X2)-1, max(X1)+1])
    plt.grid()
    plt.show()
