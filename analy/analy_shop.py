# -*- coding:utf-8 -*-
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import MySQLdb
import sys;
reload(sys);
def analy_shop(shop_id):
    sys.setdefaultencoding('utf8');
    db = MySQLdb.connect(host="localhost", user="root", passwd="okgoogle", db="dianpingshop",charset='utf8')
    cursor = db.cursor()
    sql = """select distinct content from pagecomment where shop_id = %s ;""" %shop_id
    tweets = open("keywords.txt", "w")
    cursor.execute(sql)
    for row in cursor:
       print>>tweets, row[0]
    tweets.close()
    db.close()



def seek_num(key, af_value):
    db = MySQLdb.connect("localhost","root","okgoogle","dianpingshop" )
    cursor = db.cursor()
    cursor.execute('select shopurl from dianpingshop order by %s desc limit %s' %(key,af_value))
    results = cursor.fetchall()
    temp = []
    for i in results:
        #tempInt=int(i[0])
        #print tempInt
        print i[0]

        temp.append(i[0])
    db.close()
    return temp

if __name__ == '__main__':
    shop_collection = []
    numx = int(raw_input("Please input the num of shop: "))
    shop_collection = seek_num('reviewnum', numx)
    print shop_collection
    for which_one in range(0, numx):
        print "input %s to select:" %which_one + shop_collection[which_one]
        shop_collection[which_one] = filter(lambda ch: ch in '0123456789', shop_collection[which_one])
        print  shop_collection[which_one]

    choice = int(raw_input("Please input the choice: "))
    print "you choose :" + shop_collection[choice]
    choicestr = '\'' + shop_collection[choice] + '\''
    analy_shop(choicestr)


    stopwords = {}


    # 加载stopwords
    def importStopword(filename=''):
        global stopwords
        f = open(filename, 'r')
        line = f.readline().rstrip()

        while line:
            stopwords.setdefault(line, 0)
            stopwords[line] = 1
            line = f.readline().rstrip()

        f.close()


    # 中文分词（jieba）
    def processChinese(text):
        seg_generator = jieba.cut(text)  # 使用结巴分词，也可以不使用
        seg_list = [i for i in seg_generator if i not in stopwords]
        seg_list = [i for i in seg_list if i != u' ']
        seg_list = r' '.join(seg_list)

        return seg_list


    importStopword(filename='BosonNLP_sentiment_score.txt')

    # 获取当前文件路径
    # __file__ 为当前文件, 在ide中运行此行会报错,可改为
    # d = path.dirname('.')
    d = path.dirname(__file__)
    text = open(path.join(d, 'keywords.txt')).read()  # 读取love.txt文件内容
    # 如果是中文，使用结巴分词
    text = processChinese(text)
    # 设置背景图片
    back_coloring = imread(path.join(d, "out.png"))
    # 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数
    wc = WordCloud(font_path='/System/Library/Fonts/Hiragino Sans GB W3.ttc',  # 设置字体
                   background_color="black",  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=back_coloring,  # 设置背景图片
                   # max_font_size=100, #字体最大值
                   random_state=42,
                   ).generate(text)

    # 从背景图片生成颜色值
    image_colors = ImageColorGenerator(back_coloring)

    # 绘制词云
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    plt.show()

    # 保存图片
    wc.to_file(path.join(d, "out1.png"))
