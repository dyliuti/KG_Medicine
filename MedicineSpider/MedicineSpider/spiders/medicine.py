# -*- coding: utf-8 -*-
import scrapy


class MedicineSpider(scrapy.Spider):
    name = 'medicine'
    allowed_domains = ['http://jib.xywy.com/il_sii']
    start_urls = ['http://http://jib.xywy.com/il_sii/']

    def make_requests_from_url(self, url):
        pass

    def parse(self, response):
        pass
