#coding=utf-8
# -*- coding : utf-8-*-
#! python3
from dianping.items import DianpingItem
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

class dianpingspider(Spider):
    name = 'dianping'
    allowed_domains = ['www.dianping.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

#    start_urls=[
#        'http://www.dianping.com/search/category/12/10'
#               ]
    #def parse(self, response):
    #        filename = response.url.split("/")[-2]
    #    open(filename, 'wb').write(response.body)

    def start_requests(self):
        url = 'http://www.dianping.com/search/category/12/10/o3'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item = DianpingItem()

        sel = Selector(response)
        sites = sel.xpath('//div[@id="shop-all-list"]/ul/li')
        for site in sites:
            title = site.xpath('div[2]/div[1]/a[1]/h4/text()').extract()
            item['shopname'] = title[0]
            print title[0]

            link = site.xpath('div[2]/div[1]/a[1]/@href').extract()
            item['shopurl'] = 'http://www.dianping.com' + str(link[0])
            print 'http://www.dianping.com' + str(link[0])

            shoplevels = site.xpath('div[2]/div[2]/span/@title').extract()
            item['shoplevel'] = shoplevels[0]

            reviewnums = site.xpath('div[2]/div[2]/a[1]/b/text()').extract()
            if len(reviewnums) > 0:
                item['reviewnum'] = reviewnums[0]
            else:
                item['reviewnum'] = '0'

            avgcost = site.xpath('div[2]/div[2]/a[2]/b/text()').extract()
            if len(avgcost) > 0:
                #print avgcost[0]
                #print avgcost[0].lstrip('￥')
                #print int(avgcost[0].lstrip('￥'))
                #item['avgcost'] = avgcost[0]
                item['avgcost'] = int(avgcost[0].lstrip('￥'))
            else:
                item['avgcost'] = '0'

            tastes = site.xpath('div[2]/span/span[1]/b/text()').extract()
            if len(tastes) > 0:
                item['taste'] = tastes[0]
            else:
                item['taste'] = '0'

            envs = site.xpath('div[2]/span/span[2]/b/text()').extract()
            if len(envs) > 0:
                item['env'] = envs[0]
            else:
                item['env'] = '0'

            services = site.xpath('div[2]/span/span[3]/b/text()').extract()
            if len(services) > 0:
                item['service'] = services[0]
            else:
                item['service'] = '0'

            foodtypes = site.xpath('div[2]/div[3]/a[1]/span/text()').extract()
            item['foodtype'] = foodtypes[0]

            location = site.xpath('div[2]/div[3]/a[2]/span/text()').extract()
            item['location'] = location[0]

            yield item

        nextLink = site.xpath('//div[@class="page"]/a[last()]/@data-ga-page').extract()
        print '++++++++++++++++++++++++++++++++++++++++++++++'
        print nextLink

        if nextLink:
            print nextLink[0]
            nextLink = 'http://www.dianping.com/search/category/12/10/o3p' + nextLink[0]
            #reallink = str(response.url)
            print nextLink
            #reallink = nextLink
            yield Request(nextLink, headers=self.headers)
