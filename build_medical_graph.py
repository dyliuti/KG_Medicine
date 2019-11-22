

import os, json
from py2neo import Graph, Node

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

# 疾病的属性
disease_property = [
    'name', 'desc', 'prevent', 'cause', 'easy_get', 'cure_department', 'cure_way', 'cure_lasttime', 'symptom', 'cured_prob'
]

# entities = ['Drug', 'Food', 'Check', 'Department', 'Producer', 'Symptom', 'Disease']

# entities = {
#     'symptoms': ['symptom'],
#     'departments': ['department'],     # 要从disease实体属性cure_department中获得
#     'drugs': ['recommand_drug', 'common_drug'],
#     'foods': ['not_eat', 'do_eat', 'recommand_eat'],
#     'checks':['check'],
#     'producers': ['producer'],  # 要经drug_detail -> producers
#     'diseases': ['diseases'],
# }

releation = [
    ('disease', 'symptom'),
    ('disease', 'symptom'),
]



# 实体： set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases)
# 关系： rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,\
#                rels_symptom, rels_acompany, rels_category
class MedicalGraph:
    def __init__(self):
        self.data_path = os.path.join(os.curdir, 'data/medical.json')
        self.g = Graph(host="127.0.0.1", http_port=7474, user="neo4j", password="666")

    # def get_entity_relation(self, data_json, keyword, entity, relation, relation2):
    #     if keyword in data_json:
    #         entity += data_json[keyword]
    #         for data in data_json[keyword]:
    #             relation.append([di])

    def get_entities(self, data_json):


    def read_nodes(self):
        diseases, disease = [], dict()
        # 定义实体， 共7类作为Node
        drugs = [] # 药品
        foods = [] #　食物
        checks = [] # 检查
        departments = [] #科室
        producers = [] # 药品大类（厂商）
        diseases = [] #疾病
        symptoms = []#症状

        disease_infos = []  # 疾病信息

        # 构建节点实体关系 即edge边  这里用[(a,b),(,)...]形式 元组内即对应关系 a->b
        rels_department = [] #　科室－科室关系
        rels_noteat = [] # 疾病－忌吃食物关系
        rels_doeat = [] # 疾病－宜吃食物关系
        rels_recommand_eat = [] # 疾病－推荐吃食物关系
        rels_common_drug = [] # 疾病－通用药品关系
        rels_recommand_drug = [] # 疾病－热门药品关系
        rels_check = [] # 疾病－检查关系
        rels_drug_producer = [] # 厂商－药物关系

        rels_symptom = [] #  疾病症状关系
        rels_acompany = [] # 疾病并发关系
        rels_category = [] # 疾病与科室之间的关系

        num = 0
        for data in open(self.data_path, encoding='utf-8'):
            num += 1
            data_json = json.loads(data)
            # 获取疾病属性
            for attribute in disease_property:
                if attribute in data_json:
                    disease[attribute] = data_json.get(attribute)
            # 属性中department为实体
            if 'cure_department' in disease:
                cure_department = disease['cure_department']
                if len(cure_department) == 1:
                    rels_category.append([disease, cure_department[0]])  # 疾病与科室之间的关系
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])  # 科室－科室关系
                    rels_category.append([disease, small])
                departments += cure_department
            # 获取实体
            # entity_data = {}
            # for entity, keywords in entities:
            #     for keyword in keywords:
            #     if keyword in data_json:
            #         entity_data[entity] = data_json[keyword]

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:
                    rels_acompany.append([disease, acompany])  # 疾病并发关系

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    rels_common_drug.append([disease, drug])
                drugs += common_drug

            if 'recommand_drug' in data_json:
                recommand_drug = data_json['recommand_drug']
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommand_drug.append([disease, drug])

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                do_eat = data_json['do_eat']
                recommand_eat = data_json['recommand_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])
                for _do in do_eat:
                    rels_doeat.append([disease, _do])
                for recommand in recommand_eat:
                    rels_recommand_eat.append([disease, recommand])
                foods += not_eat
                foods += do_eat
                foods += recommand_eat

            if 'check' in data_json:
                check = data_json['check']
                for _check in check:
                    rels_check.append([disease, _check])  # 检查项
                checks += check  # 总的检测项

            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                producer = [i.split('(')[0] for i in drug_detail]  # 生长商
                # 生厂商和药品
                rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
                producers += producer
            disease_infos.append(disease)

        return [set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases)], disease_infos, \
               [rels_check, rels_recommand_eat, rels_noteat, rels_doeat, rels_department, rels_common_drug, \
               rels_drug_producer, rels_recommand_drug, rels_symptom, rels_acompany, rels_category]

    '''建立节点'''   # 传入nodes列表，批量创建节点    label是节点类别名字，node_name等是节点属性
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_diseases_nodes(self, diseases):
        count = 0
        for disease_dict in diseases:
            # 类别，属性
            node = Node("Disease", disease_dict)
            # node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
            #             prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
            #             easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
            #             cure_department=disease_dict['cure_department']
            #             ,cure_way=disease_dict['cure_way'] , cured_prob=disease_dict['cured_prob'])
            # # 参数子图可以是 节点、关系、子图
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        entities, disease_infos, relations = self.read_nodes()
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases = entities
        self.create_diseases_nodes(disease_infos)
        self.create_node('Drug', Drugs) # 会有很多药、食物等节点  属性是名称
        print('Drug', len(Drugs))
        self.create_node('Food', Foods)
        print('Food', len(Foods))
        self.create_node('Check', Checks)
        print('Check', len(Checks))
        self.create_node('Department', Departments)
        print('Department', len(Departments))
        self.create_node('Producer', Producers)
        print('Producer', len(Producers))
        self.create_node('Symptom', Symptoms)
        print('Symptom', len(Symptoms))
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        entities, disease_infos, relations = self.read_nodes()
        rels_check, rels_recommand_eat, rels_noteat, rels_doeat, rels_department, rels_commond_drug, rels_drug_producer, rels_recommand_drug, rels_symptom, rels_acompany, rels_category = relations
        # 节点名称、节点名称、 关系（前个节点属性名称，后个节点属性名称）、  关系名称、 关系属性名称
        self.create_relationship('Disease', 'Food', rels_recommand_eat, 'recommand_eat', '推荐食谱')
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        self.create_relationship('Disease', 'Drug', rels_commond_drug, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        self.create_relationship('Disease', 'Drug', rels_recommand_drug, 'recommand_drug', '好评药品')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))  # node_a###node_b
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p_name = edge[0]
            q_name = edge[1]
            # p、q为节点的标签名称，rel:关系标签名称， start_node：节点名称，rel_type：关系名称，rel_name：关系属性名称
            # where指明了标签的名字（确定了节点，当然要先创建节点），然后给节点创建关系
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p_name, q_name, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''

    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        f_drug = open('drug.txt', 'w+')
        f_food = open('food.txt', 'w+')
        f_check = open('check.txt', 'w+')
        f_department = open('department.txt', 'w+')
        f_producer = open('producer.txt', 'w+')
        f_symptom = open('symptoms.txt', 'w+')
        f_disease = open('disease.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_producer.write('\n'.join(list(Producers)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()
        f_disease.close()

        return
