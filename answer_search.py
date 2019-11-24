# -*- coding: utf-8 -*-
# Author: yanminwei
# Date: 2019/11/24

from py2neo import Graph
from Common.Util import *

class AnswerSearcher:
    def __init__(self):
        self.graph = Graph(host="127.0.0.1", http_port=7474, user="dyliuti", password="666")
        self.num_limit = 20

    # 根据问题类型，返回相应的回复模板
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        for q_type, feature_name, disease_name,  ans_template in answer_template:
            if question_type == q_type:
                subject = answers[0][disease_name]
                desc = [ans[feature_name] for ans in answers]
                feature_name = '；'.join(list(set(desc))[:self.num_limit])
                final_answer = ans_template.format(disease_name=subject, feature_name=feature_name)
        # 三个例外
        if question_type == 'Disease_Cureway':
            # answer:  [{'m.name': '百日咳', 'm.cure_way': ['药物治疗', '支持性治疗']}]
            # TypeError: unhashable type: 'list' 所以要在列表中先将['药物治疗', '支持性治疗']合并
            subject = answers[0]['m.name']
            desc = [';'.join(i['m.cure_way']) for i in answers]
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'Disease_Acompany':
            subject = answers[0]['m.name']
            desc1 = [ans['n.name'] for ans in answers]
            desc2 = [ans['m.name'] for ans in answers]
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'Disease_PositiveFood':
            subject = answers[0]['m.name']
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]),
                                                                 ';'.join(list(set(recommand_desc))[:self.num_limit]))
        return final_answer

    # 执行cypher查询，并返回相应结果
    # [{'question_type': 'Disease_Cureway', 'sql': ["MATCH (m:Disease) where m.name = '感冒' return m.name, m.cureway"]}]
    def search_main(self, sqls):
        final_answers = []
        for sql in sqls:
            question_type = sql['question_type']
            queries = sql['sql']
            answers = []
            for query in queries:
                res = self.graph.run(query).data()
                answers += res
            print("answer: ", answers)
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

# sqls = [{'question_type': 'Disease_Cureway', 'sql': ["MATCH (m:Disease) where m.name = '百日咳' return m.name, m.cure_way"]}]
# handle = AnswerSearcher()
# final_answer = handle.search_main(sqls)
# print(final_answer)
