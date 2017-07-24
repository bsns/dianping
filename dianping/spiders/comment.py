# coding:utf-8
import scrapy
import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse
from scrapy.http import Request
from scrapy.http import Response
from dianping.items import CommentItem
from dianping.items import UserItem
import re
import time
from scrapy.conf import settings
import MySQLdb
import MySQLdb.cursors


class CommentSpider(scrapy.Spider):

    name = "comment"
    shop_urls = []
    cnt = 0
    page = 1
    user_home = 'http://www.dianping.com/member/'
    urls = []
    start_urls = []

    def __init__(self):
        conn = MySQLdb.connect(host="localhost",user="root",passwd="okgoogle",db="dianpingshop",charset="utf8")
        cursor = conn.cursor()
    
        cursor.execute("select shopurl from dianpingshop")


        urls = []
        shop_urls = []
        elems = cursor.fetchall()
        #for elem in cursor.fetchall():
        for elem in elems:
            #print elem
            for r in elem:
                print "44here======"
                print(r)


            str = r + '/review_more'
            print 'caling here++++' + str
                #yield self.make_requests_from_url(r[0])
            shop_urls.append(str)
            urls.append(str)

        #self.start_urls.append(urls[0])
        self.start_urls.append(urls[0])
        self.urls = urls[1:]
        self.shop_urls = shop_urls
            #yield scrapy.Request(str, callback=self.parse_item)
        #conn.commit()
        cursor.close()
        conn.close()
        #connection.close()

    def deal_num(self, str):
        ans = ''
        num = 0
        for ch in str:
            try:
                int(ch)
                num *= 10
                num += int(ch)
                break
            except:
                ans += ch

        return [ans, num]


    def user(self, response):
        temp = response.body
        soup = BeautifulSoup(temp, from_encoding='utf-8')
        item = UserItem()
        str1 = response.url
        print "1111111111111"

        id = ''
        for ch in str1:
            try:
                int(ch)
                id += ch
            except:
                pass

        item['_id'] = id

        txt = soup.find('div', class_='txt')
        item['user_name'] = txt.find('h2', class_='name').get_text().encode('utf-8')
        item['is_vip'] = 0
        try:
            vip = txt.find('div', class_='vip').find('i',class_='icon-vip')
            if vip != None:
                item['is_vip'] = 1
        except:
            pass

        col_exp = txt.find('div', class_='col-exp')
        rank = col_exp.find('span', class_='user-rank-rst')['title']
        num = 0
        for ch in rank:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['contribution'] = num

        try:
            item['gender'] = col_exp.find('span', class_='user-groun').find('i')['class'][0]
        except:
            item['gender'] = ''

        try:
            item['city'] = col_exp.find('span', class_='user-groun').get_text()
        except:
            item['city'] = ''

        try:
            msg = soup.find('div', class_='aside').find('div', class_='user-message').find('ul').find_all('li')[1].get_text()
            item['birthday'] = msg[3:]
        except:
            item['birthday'] = ''

        yield item


    def parse(self, response):
        str = response.url
        temp = response.body
        soup = BeautifulSoup(temp,"lxml", from_encoding='utf-8')
        item = CommentItem()

        try:
            id = ''
            for ch in str:
                if ch == '?':
                    break
                try:
                    int(ch)
                    id += ch
                except:
                    pass



            comment_mode = soup.find('div', class_='comment-mode')
            lists = comment_mode.find('div', class_='comment-list').find('ul').find_all('li')
            new_list = []
            for li in lists:
                try:
                    li['data-id']
                    new_list.append(li)
                except:
                    pass

            for li in new_list:


                item['shop_id'] = id
                item['_id'] = li['data-id']
                try:
                    item['user_id'] = li.find('a', class_='J_card')['user-id']
                except:
                    item['user_id'] = ''

                home = self.user_home + item['user_id']
                print response.url + '   here'
                yield Request(home, callback=self.user)

                try:
                    item['user_name'] = li.find('p', class_='name').find('a').get_text().encode('utf-8')
                except:
                    item['user_name'] = ''


                content = li.find('div', class_='content')
                user_info = content.find('div', class_='user-info')
                try:
                    stars = user_info.find('span', class_='item-rank-rst')['class']
                    tp = self.deal_num(stars[1])
                    item['stars'] = tp[1]
                except:
                    item['stars'] = ''

                try:
                    print "202here============="
                    rsts = user_info.find('div', class_='comment-rst').find_all('span', class_='rst')
                    #temp = site.xpath('//div[2]/div[1]/div/span[1]').extract()
                    tp = self.deal_num(rsts[0].get_text().encode('utf-8'))
                    #print "temp========="
                    #print temp[0]
                    #print rsts[0].get_text().encode('utf-8')
                    #print tp
                    #print tp[-1]
                    #markup = filter(lambda ch: ch in '0123456789', temp[0])
                    #print 'shoplevel=======' + shoplevels[0]
                    #item['label_1'] = int(markup)/10
                    #item['label_1'] = 1
                    #print "dict====" + dict()
                    #print "tp======" + tp
                    #print tp[0]
                    #print tp[-1]
                    item['label_1'] = tp[-1]
                    #item['label_1'] = dict()
                    #item['label_1'][tp[0]] = tp[-1]
                    print "test here219"

                    tp = self.deal_num(rsts[1].get_text().encode('utf-8'))
                    #item['label_2'] = dict()
                    #item['label_2'][tp[0]] = tp[1]
                    item['label_2'] = tp[-1]

                    tp = self.deal_num(rsts[2].get_text().encode('utf-8'))
                    #item['label_3'] = dict()
                    #item['label_3'][tp[0]] = tp[1]
                    item['label_3'] = tp[-1]
                except:
                    item['label_1'] = ''
                    item['label_2'] = ''
                    item['label_3'] = ''

                item['avg_cost'] = ''
                try:
                    cost = user_info.find('span', class_='comm-per').get_text()
                    num = 0
                    for ch in cost:
                        try:
                            int(ch)
                            num *= 10
                            num += int(ch)
                        except:
                            pass

                    item['avg_cost'] = int(num)
                except:
                    pass

                cont = content.find('div', class_='comment-txt').find('div', class_='J_brief-cont').get_text().strip()
                item['content'] = cont

                item['likes'] = []
                try:
                    dishes = content.find('div', class_='comment-recommend').find_all('a', class_='col-exp')
                    for dish in dishes:
                        item['likes'].append(dish.get_text().encode('utf-8'))

                except:
                    pass


                yield item


            print 'page: ', self.page
            self.page += 1
            try:

                next_page = soup.find('div', class_ = 'Pages').find('a', class_ = 'NextPage')
                url = self.shop_urls[self.cnt] + next_page['href']
                print 'turn page to: ' + url
                yield Request(url)
            except:
                # print '-------: ' + self.urls[self.cnt + 1]
                self.page = 1
                try:
                    time.sleep(1)
                    yield Request(self.urls[self.cnt])
                    self.cnt += 1
                except:
                    pass
        except:
            print 'oh, page error'
            time.sleep(1)
            yield Request(str, dont_filter=True)
            # pass
