# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item
import scrapy


#class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass
class DianpingItem(Item):
    shopname = Field()
    shoplevel = Field()
    shopurl = Field()
    reviewnum = Field()
    avgcost = Field()
    taste = Field()
    env = Field()
    service = Field()
    foodtype = Field()
    location = Field()

class CommentItem(scrapy.Item):
    _id = scrapy.Field()
    shop_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    stars = scrapy.Field()
    label_1 = scrapy.Field()
    label_2 = scrapy.Field()
    label_3 = scrapy.Field()
    content = scrapy.Field()
    avg_cost = scrapy.Field()
    likes = scrapy.Field()

class UserItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    is_vip = scrapy.Field()
    contribution = scrapy.Field()
    birthday = scrapy.Field()
    city = scrapy.Field()
    gender = scrapy.Field()

#class User_shopItem(scrapy.Item):
#    shopname = scrapy.Field()
#    shopurl = scrapy.Field()
#    shoplevel = scrapy.Field()

class User_shopItem(scrapy.Item):
    shopname = scrapy.Field()
    shopurl = scrapy.Field()
    shoplevel = scrapy.Field()
    _id = scrapy.Field()
