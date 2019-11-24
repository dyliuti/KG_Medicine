# -*- coding: utf-8 -*-
# Author: yanminwei
# Date: 2019/11/24

from question_classifier import *
from question_parser import *
from answer_search import *


# 问答类
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是医药智能助理dyliuti，请问有什么可以帮助您的吗？'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parse_main(res_classify)
        print(res_sql)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return "不好意思，我不清楚"
        else:
            return '\n'.join(final_answers)

# if __name__ == '__main__':
handler = ChatBotGraph()
while 1:
    question = input('用户:')
    answer = handler.chat_main(question)
    print('dyliuti:', answer)
