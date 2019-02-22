# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()            # 类别
    category2 = scrapy.Field()           # 类别2
    title = scrapy.Field()               # 名称
    goods_id = scrapy.Field()            # id
    link = scrapy.Field()                # 链接
    img_link = scrapy.Field()            # 图片链接
    price = scrapy.Field()               # 价格
    author = scrapy.Field()              # 作者
    translater = scrapy.Field()          # 翻译者
    publisher = scrapy.Field()           # 出版社
    publish_time = scrapy.Field()        # 出版时间
    detail = scrapy.Field()              # 商品详情
    abstract = scrapy.Field()            # 编辑推荐
    content = scrapy.Field()             # 内容简介
    authorIntroduction = scrapy.Field()  # 作者简介
    catalog = scrapy.Field()             # 目录
    preface = scrapy.Field()             # 前言
    mediaFeedback = scrapy.Field()       # 媒体评论
    extract = scrapy.Field()             # 免费在线读
    attachImage = scrapy.Field()         # 书摘插画
