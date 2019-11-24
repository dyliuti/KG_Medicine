
# 疾病的属性
disease_property = [
    'name', 'desc', 'prevent', 'cause', 'easy_get', 'cure_department', 'cure_way', 'cure_lasttime', 'symptom', 'cured_prob'
]
entity_name = ['Drug', 'Food', 'Check', 'Department', 'Producer', 'Symptom', 'Disease']
entity_file_name = ['drug.txt', 'food.txt', 'check.txt', 'department.txt', 'producer.txt', 'symptom.txt', 'disease.txt']

# 问句疑问词模板
symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                     '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                     '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                     '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                     '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
belong_qwds = ['属于什么科', '属于', '什么科', '科室']
cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                  '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']

# 查询的问题不包含关系的个数
NUM_NO_REL_QUESTION = 6
# 模板词--实体类型（节点类型）--问题类型
qwords_type = [
    [cause_qwds,    'Disease',  'Disease_Cause'],
    [prevent_qwds,  'Disease',  'Disease_Prevent'],
    [lasttime_qwds, 'Disease',  'Disease_Lasttime'],
    [cureway_qwds,  'Disease',  'Disease_Cureway'],
    [cureprob_qwds, 'Disease',  'Disease_Cureprob'],
    [easyget_qwds,  'Disease',  'Disease_Easyget'],

    [symptom_qwds,  'Disease',  'Disease_Symptom'],
    [symptom_qwds,  'Symptom',  'Symptom_Disease'],
    [acompany_qwds, 'Disease',  'Disease_Acompany'],
    [drug_qwds,     'Disease',  'Disease_Drug'],
    [cure_qwds,     'Drug',     'Drug_Disease'],
    [check_qwds,    'Disease',  'Disease_Check'],
    [check_qwds,    'Check',    'Check_Disease'],
    [cure_qwds,     'Check',    'Check_Disease'],
]
#     [food_qwds,      'Disease', 'Disease_PositiveFood'],    # 已知疾病找实物
#     [food_qwds,      'Disease', 'Disease_NegativeFood'],
#     [food_qwds,      'Food',    'PositiveFood_Disease'],        # 已知实物找对应疾病
#     [food_qwds,      'Food',    'NegativeFood_Disease'],
#     [cure_qwds,      'Food',    'PositiveFood_Disease'],
#     [cure_qwds,      'Food',    'NegativeFood_Disease'],

# 关系-节点名称（实体名称）-问题类型
query_rels = [
    ['Disease_Symptom',     'has_symptom',      'Symptom'],
    ['Symptom_Disease',     'has_symptom',      'Symptom'],
    ['Disease_Acompany',    'acompany_with',    'Disease'],
    ['Disease_Drug',        'common_drug',      'Drug'],
    ['Disease_Drug',        'recommand_drug',   'Drug'],
    ['Drug_Disease',        'common_drug',      'Drug'],
    ['Drug_Disease',        'recommand_drug',   'Drug'],
    ['Disease_Check',       'need_check',       'Check'],
    ['Check_Disease',       'need_check',       'Check'],

    ['Disease_PositiveFood', 'do_eat',          'Food'],
    ['Disease_PositiveFood', 'recommand_eat',   'Food'],
    ['Disease_NegativeFood', 'no_eat',          'Food'],
    ['PositiveFood_Disease', 'do_eat',          'Food'],
    ['PositiveFood_Disease', 'recommand_eat',   'Food'],
    ['NegativeFood_Disease', 'no_eat',          'Food'],
]
# 下面这两种关系是多余的
#     ['drugs_of', ''],
#     ['belongs_to', ''],
def remove_punc(text):
    return text.replace('\r' ,'').replace('\n' ,'').replace('\xa0', ' ').replace('   ', '').replace('\t' ,'')
