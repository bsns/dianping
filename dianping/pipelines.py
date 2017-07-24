# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json
from scrapy import Field,Item
import scrapy
from items import DianpingItem
from items import CommentItem
from items import UserItem
from dianping.items import User_shopItem




class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('info.json', 'w', encoding='utf-8')#保存为json文件
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"#转为json的
        self.file.write(line)#写入文件中
        return item
    def spider_closed(self, spider):#爬虫结束时关闭文件
        self.file.close()

class DianpingPipeline(object):
    #def process_item(self, item, spider):
    #    return item

    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparams=dict(
            host=settings['MYSQL_HOST'],#读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)#相当于dbpool付给了这个类，self中可以得到


    def process_item(self, item, spider):
        if isinstance(item, DianpingItem):
            query=self.dbpool.runInteraction(self._conditional_insert,item)#调用插入的方法
            query.addErrback(self._handle_error,item,spider)#调用异常处理方法
        elif isinstance(item, User_shopItem):
            query=self.dbpool.runInteraction(self._conditional_insert_User_shopItem,item)#调用插入的方法
            query.addErrback(self._handle_error,item,spider)
            print item
            print 'User_shopItem'
        #if isinstance(item, UserItem):
        #    query=self.dbpool.runInteraction(self._conditional_insert_User,item)#调用插入的方法
        #    query.addErrback(self._handle_error,item,spider)
        #    print item
        #    print 'itemuser'
        #if isinstance(item, User_shopItem):
        #    query=self.dbpool.runInteraction(self._conditional_insert_User_shopItem,item)#调用插入的方法
        #    query.addErrback(self._handle_error,item,spider)
        #    print item
        #    print 'User_shopItem'
        elif spider.name == 'comment':
            str1 = type(item)
            print "type=======" + str(str1)
            if str(str1) == "<class 'dianping.items.CommentItem'>":
                query=self.dbpool.runInteraction(self._conditional_insert_Comment,item)#调用插入的方法
                query.addErrback(self._handle_error,item,spider)
                print item
                print 'CommentItem'
            else:
                query=self.dbpool.runInteraction(self._conditional_insert_User,item)#调用插入的方法
                query.addErrback(self._handle_error,item,spider)
                print item
                print 'itemuser'

        return item


    def _conditional_insert(self, tx, item):

        sql = "insert into yangzhoushop(shopname,shoplevel,shopurl,reviewnum,avgcost,taste,env,service,foodtype,location) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item['shopname'], item['shoplevel'], item['shopurl'], item['reviewnum'],item['avgcost'],item['taste'],item['env'],item['service'],item['foodtype'],item['location'])
        tx.execute(sql, params)
    def _conditional_insert_User(self, tx, item):
        sql = "insert into user(city,gender,birthday,is_vip,contribution,_id,user_name) values(%s,%s,%s,%s,%s,%s,%s)"
        params = (item['city'], item['gender'], item['birthday'], item['is_vip'], item['contribution'], item['_id'], item['user_name'])
        tx.execute(sql, params)
#    def _conditional_insert_Comment(self, tx, item):
#        sql = "insert into pagecomment(content,user_id,stars,avg_cost,shop_id,label_1,label_2,label_3,_id,user_name,likes) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#        params = (item['content'], item['user_id'], item['stars'], item['avg_cost'], item['shop_id'], item['label_1'], item['label_2'], item['label_3'], item['_id'], item['user_name'], item['likes'])
#        tx.execute(sql, params)
    def _conditional_insert_Comment(self, tx, item):
        try:
            #sql = "insert into pagecomment(content,user_id,stars,avg_cost,shop_id,label_1,label_2,label_3,_id,user_name,likes) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #params = (item['content'], item['user_id'], item['stars'], item['avg_cost'], item['shop_id'], item['label_1'], item['label_2'], item['label_3'], item['_id'], item['user_name'], item['likes'])
            sql = "insert into pagecomment(content,user_id,stars,avg_cost,shop_id,label_1,label_2,label_3,_id,user_name) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (item['content'], item['user_id'], item['stars'], item['avg_cost'], item['shop_id'], item['label_1'], item['label_2'], item['label_3'], item['_id'], item['user_name'])
            tx.execute(sql, params)
            #self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        #return item
    def _conditional_insert_User_shopItem(self, tx, item):
        sql = "insert into user_shop(shopname,shopurl,shoplevel,_id) values(%s,%s,%s,%s)"
        params = (item['shopname'], item['shopurl'], item['shoplevel'], item['_id'])
        tx.execute(sql, params)

    def _handle_error(self, failue, item, spider):
        print failue
