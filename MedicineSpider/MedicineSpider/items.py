# -*- coding: utf-8 -*-
# Authon: yanminwei
# Date: 2019/11/18

import scrapy
from scrapy import Field

class MedicinespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    basic_info = Field()
    cause_info = Field()
    prevent_info = Field()
    symptom_info = Field()
    inspect_info = Field()
    treat_info = Field()
    food_info = Field()
    drug_info = Field()

