# -*- coding: utf-8 -*-
# Authon: yanminwei
# Date: 2019/11/18

import scrapy
from scrapy import Request
from MedicineSpider.items import MedicinespiderItem
from Util import *

class MedicineSpider(scrapy.Spider):
    name = 'medicine'
    # 包含了爬取的域名，不在域名中的request不被允许
    allowed_domains = ['http://jib.xywy.com/il_sii']

    def __init__(self):
        super(MedicineSpider, self).__init__()
        self.route = [
            # 请求页面， 页面关键字， 存数据库的键值， 请求应答解析函数
            ['http://jib.xywy.com/il_sii/gaishu/{index}.htm',  'gaishu',  'basic_info',   self.parse_gaishu],
            ['http://jib.xywy.com/il_sii/cause/{index}.htm',   'cause',   'cause_info',   self.common_parse],
            ['http://jib.xywy.com/il_sii/prevent/{index}.htm', 'prevent', 'prevent_info', self.common_parse],
            ['http://jib.xywy.com/il_sii/symptom/{index}.htm', 'symptom', 'symptom_info', self.parse_symptom],
            ['http://jib.xywy.com/il_sii/inspect/{index}.htm', 'inspect', 'inspect_info', self.parse_inspect],
            ['http://jib.xywy.com/il_sii/treat/{index}.htm',   'treat',   'treat_info',   self.parse_treat],
            ['http://jib.xywy.com/il_sii/food/{index}.htm',    'food',    'food_info',    self.parse_food],
            ['http://jib.xywy.com/il_sii/drug/{index}.htm',    'drug',    'drug_info',    self.parse_drug],
        ]
        self.item = MedicinespiderItem()
        self.num = 0

    def start_requests(self):
        for url, _, _, _ in self.route:
            print("url: ", url.format(index=1))
            yield Request(url=url.format(index=1))

    # 1.可返回item；2.可再生成request
    def parse(self, response):
        elem = response.xpath(r'//meta[@http-equiv="mobile-agent"]/@content').extract_first().split('/')[-2]
        for _, k, key, handler in self.route:
            if k == elem:
                self.item[key] = handler(response)
                break
        self.num += 1
        if self.num % len(self.route) == 0:
            yield self.item
            self.item.clear()
            index = int(self.num / len(self.route) + 1)
            if index  >= 2:
                return
            for url, _, _, _ in self.route:
                print("url: ", url.format(index=index))
                yield Request(url=url.format(index=index), dont_filter=True)

    '''概述'''
    def parse_gaishu(self, response):
        basic_info = dict()
        basic_info['name'] = response.xpath('//title/text()').extract_first().split('的简介')[0]
        basic_info['category'] = response.xpath('//div[@class="wrap mt10 nav-bar"]/a').xpath('string(.)').extract()
        descs = response.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()').extract()
        basic_info['desc'] = [remove_punc(desc) for desc in descs]
        p_tags = response.xpath('//div[@class="mt20 articl-know"]/p').xpath('string(.)').extract()
        basic_info['attributes'] = [remove_punc(p_tag) for p_tag in p_tags if '：' in p_tag]
        return basic_info

    '''病因、预防'''
    def common_parse(self, response):
        p_tags = response.xpath(r'//p').xpath('string(.)').extract()
        infobox = []
        for p_tag in p_tags:
            info = remove_punc(p_tag)
            if info:
                infobox.append(info)
        return '\n'.join(infobox)

    '''症状'''
    def parse_symptom(self, response):
        # results = re.findall('<p>.*?\d+.(.*?)<.*?ank">(.*?)</a>', response.text, re.S)
        symptoms = response.xpath('//span[@class="db f12 lh240 mb15 "]/a').xpath('string(.)').extract() # /text()
        print("symptoms",symptoms)
        p_tags = response.xpath('//p').xpath('string(.)').extract()
        detail = [remove_punc(p_tag) for p_tag in p_tags]
        return dict(symptoms=symptoms, symptoms_detail=detail)

    '''检查'''
    def parse_inspect(self, response):
        return response.xpath('//li[@class="check-item"]/a/@href').extract()

    '''治疗'''
    def parse_treat(self, response):
        p_tags = response.xpath('//div[starts-with(@class,"mt20 articl-know")]/p').xpath('string(.)').extract() # text()
        return [remove_punc(p_tag) for p_tag in p_tags]

    '''饮食'''
    def parse_food(self, response):
        div_tags = response.xpath('//div[@class="diet-img clearfix mt20"]')
        good = div_tags[0].xpath('./div/p/text()').extract()
        bad = div_tags[1].xpath('./div/p/text()').extract()
        recommand = div_tags[2].xpath('./div/p/text()').extract()
        return dict(good=good, bad=bad, recommand=recommand)

    '''药品'''
    def parse_drug(self, response):
        a_tags = response.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()').extract()
        return [remove_punc(a_tag) for a_tag in a_tags]


