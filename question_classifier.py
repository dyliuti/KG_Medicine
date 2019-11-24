# -*- coding: utf-8 -*-
# Author: yanminwei
# Date: 2019/11/21

import os
import ahocorasick
from Common.Util import *


class QuestionClassifier:
    def __init__(self):
        self.root_path = os.path.join(os.curdir, 'Data\dict')
        self.drug_wds, self.food_wds, self.check_wds, self.department_wds, self.producer_wds, self.symptom_wds, self.disease_wds = [],[],[],[],[],[],[]
        self.feature_wds = [self.drug_wds, self.food_wds, self.check_wds, self.department_wds, self.producer_wds, self.symptom_wds, self.disease_wds]
        # 加载特征词, 并用特征词构成领域词
        self.domain_words = []
        for i, file_name in enumerate(entity_file_name):    # zip(self.feature_wds, entity_file_name)有点问题
            self.feature_wds[i] = [i.strip().replace('.', '') for i in open(os.path.join(self.root_path, file_name), encoding='utf-8') if i.strip()]
            self.domain_words += self.feature_wds[i]
        # 否定词
        self.deny_path = os.path.join(self.root_path, 'deny.txt')
        self.deny_words = [i.strip() for i in open(self.deny_path, encoding='utf-8') if i.strip()]
        # 特征词构成领域专业词
        self.domain_words = set(self.domain_words)
        # 构造领域actree  两种数据结构：trie和Aho-Corasick自动机
        self.domain_tree = self.build_actree(list(self.domain_words))
        # 构建词典 词对应的类型
        self.wdtype_dict = self.build_wdtype_dict()  # 遍历self.domain_words（抽取到的实体） 看属于哪个实体（7个）属性名称

    '''构造actree，加速过滤'''  # 多模式匹配，方便匹配领域关键字
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''构造每个领域词对应的节点类型'''
    def build_wdtype_dict(self):
        word_dict = dict()
        for word in self.domain_words:
            word_dict[word] = []
            # entity_name = ['Drug', 'Food', 'Check', 'Department', 'Producer', 'Symptom', 'Disease']
            # 每个特征词集与实体名称（节点类型）一一对应
            for feature_words, node_name in zip(self.feature_wds, entity_name):
                if word in feature_words:
                    word_dict[word].append(node_name)
        return word_dict

    # Actree提取领域词及其对应的节点名称
    def extract_domain_word(self, question):
        domain_words = []
        for i in self.domain_tree.iter(question):   # 将AC_KEY中的每一项与content内容作对比，若匹配则返回
            word = i[1][1]
            # print(i)    # (1, (32433, '耳鸣'))  第几个  value(end_index, value)
            # print('word: ', word)
            domain_words.append(word)
        # 同类词保留字多的
        stop_words = []
        for word1 in domain_words:
            for word2 in domain_words:
                if word1 in word2 and word1 != word2:
                    stop_words.append(word1)
        final_words = [word for word in domain_words if word not in stop_words]
        # 领域词（节点属性名称）->节点名称
        domain_word2type = {word: self.wdtype_dict.get(word) for word in final_words}
        return domain_word2type

    # 使用模板匹配方法
    def check_words(self, template_words, question):
        for word in template_words:
            if word in question:
                return True
        return False

    '''问题分类'''
    # 主要得到args（多模式匹配出提问包含的关键字-对应接地那类型）和 question_types（问题类型）
    def classify(self, question):
        domain_word2type = self.extract_domain_word(question)
        print("Actree result: ", domain_word2type)
        if not domain_word2type:
            return {}
        data = dict()
        data['args'] = domain_word2type
        # 问句中涉及的所有实体类型
        types = []
        for type_ in domain_word2type.values(): # values 是list的list  {'百日咳': ['Disease']}
            types += type_

        question_type = 'Others'
        question_types = []
        # 不包括最后6个关于food的特征词
        for template_words, node_name, question_type, _ in qwords_type[:NUM_FOOD_QUESTION]:
            if node_name in types and self.check_words(template_words, question):
                # print(question_type)
                question_types.append(question_type)

        # 推荐食品
        if self.check_words(food_qwds, question) and 'Disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'Disease_NegativeFood'
            else:
                question_type = 'Disease_PositiveFood'
            question_types.append(question_type)

        # 已知食物找疾病
        if self.check_words(food_qwds + cure_qwds, question) and 'Food' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'NegativeFood_Disease'
            else:
                question_type = 'PositiveFood_Disease'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'Disease' in types:
            question_types = ['Disease_Desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['Symptom_Disease']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data

# handler = QuestionClassifier()
# while 1:
#     question = input('input an question:')
#     data = handler.classify(question)
#     print(data)

