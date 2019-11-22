# -*- coding: utf-8 -*-
# 将爬虫得到的数据进行进一步提取得到本体


import pymongo, os
from Common.max_cut import *

attr_key_word = {
            "医保疾病" : 'yibao_status',
            "患病比例" : "get_prob",
            "易感人群" : "easy_get",
            "传染方式" : "get_way",
            "并发症": 'acompany',
            "就诊科室" : "cure_department",
            "治疗方式" : "cure_way",
            "治疗周期" : "cure_lasttime",
            "治愈率" : "cured_prob",
            "常用药品": 'common_drug',
            "治疗费用": 'cost_money',
}

class OntologyExtract:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['dyliuti']
        self.collection = self.db['dyliuti']
        self.cuter = CutWords(file_path=os.path.join(os.curdir, 'Data/dict/disease.txt'))

    def __handle_attributes(self, data, attributes):
        if not attributes:
            return
        for attr in attributes:
            attr_pair = attr.split('：')
            if len(attr_pair) == 2:  # 防异常
                key = attr_pair[0].replace(" ", "")
                value = attr_pair[1].strip()    # 先去除两端空格，split后不用判断空
                if key in ["医保疾病","患病比例", "易感人群", "传染方式", "治疗周期", "治疗方式", "治疗费用"]:
                    data[attr_key_word[key]] = value.replace(" ", "")
                if key in ["就诊科室", "治疗方式", "常用药品"]:
                    data[attr_key_word[key]] = value.split()
                if key in ["并发症"]:
                    print(value)
                    acompany = [i for i in self.cuter.max_biward_cut(value) if len(i) > 1]
                    data[attr_key_word[key]] = acompany

    def __handle_food(self, data, food_info):
        if not food_info:
            return
        if food_info.get('recommand', None) is not None:
            data['recommand_eat'] = food_info['recommand']
        if food_info.get('good', None) is not None:
            data['not_eat'] = food_info['good']
        if food_info.get('bad', None) is not None:
            data['do_eat'] = food_info['bad']

    def collect_ontology(self):
        data = dict()
        num = 0
        for item in self.collection.find():
            num += 1
            basic_info = item['basic_info']
            name = basic_info['name']
            if not name: # name is ""
                continue
            data['_id'] = num
            data['name'] = name
            data['desc'] = '\n'.join(basic_info['desc']).replace(" ", "").replace("\n", "")
            data['category'] = basic_info['category']
            self.__handle_attributes(data, basic_info['attributes'])
            data['prevent'] = item.get('prevent_info')
            data['cause'] = item.get('cause_info')
            symptom_info = item.get('symptom_info')
            if symptom_info:
                data['symptom'] = symptom_info.get('symptoms')
            data['inspect'] = item.get('inspect_info')
            self.__handle_food(data, item.get('food_info'))
            drug_info = item.get('drug_info')
            if drug_info:
                data['recommand_drug'] = list(set([drug.split('(')[-1].replace(')','') for drug in drug_info]))
                data['drug_detail'] = drug_info

            try:
                self.db['medical'].insert(data)
                print(num)
            except Exception as e:
                print(e)

med = OntologyExtract()
med.collect_ontology()


