# -*- coding: utf-8 -*-
import json
import re

import requests
import scrapy
from fake_useragent import UserAgent
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from dangdang.items import DangdangItem

ua = UserAgent()


class BooksSpider(CrawlSpider):
    name = 'books'
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_FILE': 'warn.log',
        'LOG_LEVEL': 'WARNING'
    }
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/']

    rules = (
        Rule(LinkExtractor(
            allow=r'/cp01.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.html$'), follow=True),
        Rule(LinkExtractor(allow=r'product.dangdang.com/\d+.html$', restrict_xpaths=("//p[@class='name']/a")),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = DangdangItem()
        # 类别
        item['category'] = response.xpath(
            '//*[@id="breadcrumb"]/a[2]/text()').get(default='')
        # 类别2
        item['category2'] = response.xpath(
            '//*[@id="breadcrumb"]/a[3]/text()').get(default='')
        # 名称
        item['title'] = response.xpath(
            "//*[@id='product_info']/div[1]/h1/@title").get(default='')
        goods_id = re.compile(r'/(\d+).html').findall(response.url)[0]
        # id
        item['goods_id'] = goods_id
        # 链接
        item['link'] = response.url
        # 图片链接
        item['img_link'] = response.xpath(
            '//div[@class="img_list"]/ul//li/a/@data-imghref').getall()
        # 价格
        try:
            item['price'] = response.xpath(
                '//*[@id="dd-price"]/text()').getall()[1].strip()
        except IndexError:
            item['price'] = response.xpath(
                '//*[@id="dd-price"]/text()').getall()[0].strip()
        # 作者
        item['author'] = response.xpath('//*[@id="author"]/a/text()').getall()
        # 翻译者
        item['translater'] = response.xpath(
            '//*[@id="author"]/a[4]/text()').get(default='')
        # 出版社
        item['publisher'] = response.xpath(
            '//*[@id="product_info"]/div[2]/span[2]/a/text()').get(default='')
        # 出版时间
        item['publish_time'] = response.xpath(
            '//*[@id="product_info"]/div[2]/span[3]/text()').get(default='')
        # 商品详情
        item['detail'] = response.xpath(
            '//*[@id="detail_describe"]/ul//li/text()').getall()

        script = response.xpath("/html/body/script[1]/text()").get()
        categoryPath = re.compile(
            r'.*categoryPath":"(.*?)","describeMap').findall(script)[0]
        url = "http://product.dangdang.com/index.php?r=callback%2Fdetail&productId={0}&templateType=publish&describeMap=&shopId=0&categoryPath={1}".format(
            goods_id, categoryPath)
        headers = {
            'User-Agent': ua.chrome,
            'Connection': 'close',
        }
        result = requests.get(url, headers=headers)
        text = result.json().get('data').get('html')
        html = etree.HTML(text)
        if html is None:
            item['abstract'] = ''
            item['content'] = ''
            item['authorIntroduction'] = ''
            item['catalog'] = ''
            item['preface'] = ''
            item['mediaFeedback'] = ''
            item['extract'] = ''
            item['attachImage'] = ''
        else:
            # 编辑推荐
            try:
                if html.xpath('//*[@id="abstract"]/div[1]/span/text()')[0] == '编辑推荐':
                    item['abstract'] = re.compile(
                        r'<span>编辑推荐</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['abstract'] = ''
            # 内容简介
            try:
                if html.xpath('//*[@id="content"]/div[1]/span/text()')[0] == '内容简介':
                    item['content'] = re.compile(
                        r'<span>内容简介</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['content'] = ''
            # 作者简介
            try:
                if html.xpath('//*[@id="authorIntroduction"]/div[1]/span/text()')[0] == '作者简介':
                    item['authorIntroduction'] = re.compile(
                        r'<span>作者简介</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['authorIntroduction'] = ''
            # 目录
            try:
                if html.xpath('//*[@id="catalog"]/div[1]/span/text()')[0].replace('\u3000', '') == '目录':
                    item['catalog'] = re.compile(
                        r'<span>目\u3000\u3000录</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['catalog'] = ''
            # 前言
            try:
                if html.xpath('//*[@id="preface"]/div[1]/span/text()')[0].replace('\u3000', '') == '前言':
                    item['preface'] = re.compile(
                        r'<span>前\u3000\u3000言</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['preface'] = ''
            # 媒体评论
            try:
                if html.xpath('//*[@id="mediaFeedback"]/div[1]/span/text()')[0] == '媒体评论':
                    item['mediaFeedback'] = re.compile(
                        r'<span>媒体评论</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['mediaFeedback'] = ''
            # 免费在线读
            try:
                if html.xpath('//*[@id="extract"]/div[1]/span/text()')[0] == '免费在线读':
                    item['extract'] = re.compile(
                        r'<span>免费在线读</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['extract'] = ''
            # 书摘插画
            try:
                if html.xpath('//*[@id="attachImage"]/div[1]/span/text()')[0] == '书摘插画':
                    item['attachImage'] = re.compile(
                        r'<span>书摘插画</span></div><div class="descrip">(.*?)</div>', re.S).findall(text)[0]
            except IndexError:
                item['attachImage'] = ''
        yield item
