#coding:utf-8
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

mean_values = [39, 35, 21, 15, 331, 31, 25, 6, 22, 22, 24, 16, 72, 10, 36]
variance = [0.2, 0.4, 0.5, 0.2, 0.4, 0.2, 0.4, 0.5, 0.2, 0.4, 0.2, 0.4, 0.5, 0.2, 0.4]
bar_labels = [u'三盛广场', u'京华城', u'扬子江路', u'扬州大学', u'邗江区', u'文汇西路', u'望月路', u'来鹤台广场', u'梅岭', u'汊河汇金谷', u'汽车西站', u'沃尔玛', u'瘦西湖', u'秋雨路', u'其它']
x_pos = list(range(len(bar_labels)))
plt.bar(x_pos, mean_values, yerr=variance, align='center', alpha=0.5)

plt.grid()

max_y = max(zip(mean_values, variance)) # returns a tuple, here: (3, 5)
plt.ylim([0, (max_y[0] + max_y[1]) * 1.1])

plt.ylabel('variable y')
plt.xticks(x_pos, bar_labels)
plt.title(u'扬州')

plt.show()
#plt.savefig('./my_plot.png')
