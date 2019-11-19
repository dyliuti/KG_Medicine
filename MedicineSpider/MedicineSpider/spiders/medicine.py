# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
from MedicineSpider.items import MedicinespiderItem
from Util import *

class MedicineSpider(scrapy.Spider):
    name = 'medicine'
    # 包含了爬取的域名，不在域名中的request不被允许
    allowed_domains = ['http://jib.xywy.com/il_sii']

    start_urls = [
        'http://jib.xywy.com/il_sii/gaishu/{index}.htm',
        'http://jib.xywy.com/il_sii/cause/{index}.htm',
        'http://jib.xywy.com/il_sii/prevent/{index}.htm',
        'http://jib.xywy.com/il_sii/symptom/{index}.htm',
        # 'http://jib.xywy.com/il_sii/inspect/{index}.htm',
        # 'http://jib.xywy.com/il_sii/treat/{index}.htm',
        # 'http://jib.xywy.com/il_sii/food/{index}.htm',
        # 'http://jib.xywy.com/il_sii/drug/{index}.htm',
    ]


    def __init__(self):
        super(MedicineSpider, self).__init__()
        self.route = [
            ['gaishu', 'basic_info', self.parse_gaishu],
            ['cause', 'cause_info', self.common_parse],
            ['prevent', 'prevent_info', self.common_parse],
            ['symptom', 'symptom_info', self.parse_symptom],
            ['inspect', 'inspect_info', self.parse_inspect],
            ['treat', 'treat_info', self.parse_treat],
            ['food', 'food_info', self.parse_food],
            ['drug', 'drug_info', self.parse_drug],
        ]
        self.item = MedicinespiderItem()
        self.num = 0

    def start_requests(self):
        for url in self.start_urls:
            print("url: ", url.format(index=1))
            yield Request(url=url.format(index=1))

    # 1.可返回item；2.可再生成request
    def parse(self, response):
        elem = response.xpath(r'//meta[@http-equiv="mobile-agent"]/@content').extract_first().split('/')[-2]
        for k, key, handler in self.route:
            if k == elem:
                self.item[key] = handler(response)
                break
        self.num += 1
        if self.num % len(self.start_urls) == 0:
            yield self.item
            self.item.clear()
            index = int(self.num / len(self.start_urls) + 1)
            if index  >= 2:
                return
            for url in self.start_urls:
                print("url: ", url.format(index=index))
                yield Request(url=url.format(index=index), dont_filter=True)

    '''概述'''
    def parse_gaishu(self, response):
        selector = Selector(response=response)
        basic_info = dict()
        basic_info['name'] = selector.xpath('//title/text()').extract_first().split('的简介')[0]
        basic_info['category'] = selector.xpath('//div[@class="wrap mt10 nav-bar"]/a').xpath('string(.)').extract()
        descs = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()').extract()
        basic_info['desc'] = [remove_punc(desc) for desc in descs]
        p_tags = selector.xpath('//div[@class="mt20 articl-know"]/p').xpath('string(.)').extract()
        basic_info['attributes'] = [remove_punc(p_tag) for p_tag in p_tags]
        return basic_info

    # 病因、预防
    def common_parse(self, response):
        selector = Selector(response=response)
        p_tags = selector.xpath(r'//p').xpath('string(.)').extract()
        infobox = []
        for p_tag in p_tags:
            info = remove_punc(p_tag)
            if info:
                infobox.append(info)
        return '\n'.join(infobox)


    '''并发症'''
    def parse_symptom(self, response):
        pass

    '''检查'''
    def parse_inspect(self, response):
        pass

    '''治疗'''
    def parse_treat(self, response):
        pass

    '''饮食'''
    def parse_food(self, response):
        pass

    '''药品'''
    def parse_drug(self, response):
        pass


