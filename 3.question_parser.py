# -*- coding: utf-8 -*-
from Common.Util import *

class QuestionPaser:
    '''构建实体节点'''
    # 输入例子 {'耳鸣': ['Disease', 'Symptom']}
    # 输出例子 {'Disease': ['耳鸣'], 'Symptom': ['耳鸣']}
    def build_entity2feature(self, args):
        entity2feature = {}
        for feature, types in args.items():
            for type_ in types:
                if type_ not in entity2feature:
                    entity2feature[type_] = [feature]
                else:
                    entity2feature[type_].append(feature)
        return entity2feature

    # 针对不同的问题，分开进行处理
    def sql_transfer(self, question_type, features):
        if not features:
            return []

        sql = list()
        # 查询疾病属性(无关系)的sql查询模板
        sql_template = "MATCH (m:Disease) where m.name = '{name}' return m.name, m.{property}"
        for _, node_name, q_type, property_ in qwords_type[:NUM_NO_REL_QUESTION]:
            if question_type == q_type:
                sql = [sql_template.format(name=feature, property=property_) for feature in features]

        # 查询疾病的属性-描述  特殊的没在qwords_type中
        if question_type == 'Disease_Desc':
            sql = [sql_template.format(name=feature, property='desc') for feature in features]

        # 查询有关系的实体
        sql_template = "MATCH (m:Disease)-[r:{rel}]->(n:{node_name}) where n.name = '{name}' return m.name, r.name, n.name"
        for q_type, rel, node_name in query_rels:
            if question_type == q_type:
                sql = [sql_template.format(rel=rel, node_name=node_name, name=feature) for feature in features]

        return sql


    # res_classify: question_classifer解析得到的结果data
    # 输入例子 {'args': {'耳鸣': ['Disease', 'Symptom']}, 'question_types': ['Disease_PositiveFood']}
    def parse_main(self, res_classify):
        args = res_classify['args']
        entity2feature = self.build_entity2feature(args)
        print("entity_dict: ", entity2feature)
        question_types = res_classify['question_types']
        print("question_types: ", question_types)
        sqls = []
        for question_type in question_types:
            sql, sql_list = dict(), list()
            sql['question_type'] = question_type
            for _, node_name, q_type, _ in qwords_type:
                if question_type == q_type:
                    sql_list = self.sql_transfer(question_type=question_type, features=entity2feature.get(node_name))

            if sql_list:
                sql['sql'] = sql_list
                sqls.append(sql)

        return sqls

res_classify = dict({'args': {'百日咳': ['Disease']}, 'question_types': ['Disease_Cureway']})
handler = QuestionPaser()
sqls = handler.parse_main(res_classify)
print(sqls)
