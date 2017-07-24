#coding=utf-8
# -*- coding : utf-8-*-

from dianping.items import User_shopItem
from dianping.items import CommentItem
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import sys
import MySQLdb
import MySQLdb.cursors


reload(sys)
sys.setdefaultencoding('utf-8')


class dianpingspider(Spider):
    name = 'user'
    allowed_domains = ['www.dianping.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }


    def start_requests(self):
        conn = MySQLdb.connect(user='root', passwd='okgoogle', db='dianpingshop', host='localhost', charset="utf8", use_unicode=True)
        cursor = conn.cursor()
        cursor.execute('SELECT _id FROM user;')
        print cursor.execute("SELECT _id FROM user")
        print "38================"
        rows = cursor.fetchall()

        for row in rows:
            if row:
                print row[0]
                #global temp
                #temp = row[0]
                row = "https://www.dianping.com/member/" + str(row[0]) + "/reviews"
                print row
                #temp = row
                yield Request(row, self.parse, meta=dict(start_url=row))
        cursor.close()


    def parse(self, response):
        item = User_shopItem()

        sel = Selector(response)
        sites = sel.xpath('//div[@id="J_review"]/div[1]/ul/li')
        #print sel.xpath('//div[@id="J_review"]')
        for site in sites:
            print site
            print "42-----------"
            #print site.xpath('//div/div[1]/h6/a/text()').extract()
            title = site.xpath('div/div[1]/h6/a/text()').extract()
            item['shopname'] = title[0]
            print title[0]

            link = site.xpath('//div/div[1]/h6/a/@href').extract()
            item['shopurl'] = str(link[0])
            print str(link[0])

            shoplevels = site.xpath('//div[1]/ul/li[*]/div/div[2]/div[2]/span').extract()
            markup = filter(lambda ch: ch in '0123456789', shoplevels[0])

            #print 'shoplevel=======' + shoplevels[0]
            item['shoplevel'] = int(markup)/10

            #temp = filter(lambda ch: ch in '0123456789', response.url)
            id = ''
            for ch in response.url:
                if ch == '?':
                    break
                try:
                    int(ch)
                    id += ch
                except:
                    pass
            #_id = id
            #print "_id====" + temp
            item['_id'] = id
            yield item

        #print site.xpath('//div[@class="pages-num"]/@page-next/a[last()]/@data-pg').extract()
        print response.url
        print '++++++++++++++++++++++++++++++++++++++++++++++'

        #print temp
        nextLink = site.xpath('//div[@class="pages-num"]/a[last()][@class="page-next"]/@data-pg').extract()

        print nextLink

        if nextLink:
            print nextLink[0]
            nextLink = response.url + '?pg=' + nextLink[0]
            #reallink = str(response.url)
            print nextLink
            #reallink = nextLink
            yield Request(nextLink, headers=self.headers)
