**“纸上得来终觉浅，绝知此事要躬行。”  —— 陆游**

**"Practice，practice，practice and summary makes perfect" —— dyliuti**

------



**感谢：**

这一年感谢真正富有学识，又乐于分享的大神们。你们总是在想能给予别人什么，怎么成就别人，让人敬佩。也感谢可能素不相识，却给过我鼓励的人们，谢谢了！我的微信yanminweilalala，若想交个朋友或进一步交流可以加我微信。

<br>

**医药领域知识图谱：**

发现特定领域的知识图谱，用模板来实现还是挺简洁的。虽然模板会被诟病为维护难、难扩展，给人死板的印象。但仔细分析数据类型、查询语句的结构，还是能提取到许多共同点。这些共同点可用于实体、属性、关系的扩展。

实体数量：4万4左右。

关系数量：29万左右。

<br>

**文件说明：**

一、MedicineSpider：使用scrapy进行医药数据爬取，存储到MongoDb中。

二、0.extract_ontology.py：将爬取保存到MongoDB的数据进行二次处理，得到更简洁的数据存到MongoDB。

三、1.build_medical_graph.py：创建实体、属性、关系，建立医药领域知识图谱，保存到neo4j中。

四、question_classifier.py：利用模板关键词，构建Actree作索引，对用户的提问进行分类。

五、question_parser.py：对用户的提问类别，组成对应的查询语句。

六、answer_search.py：根据问题类别，制作相应的回答模板。将查询得到的结果放入模板中。

七、5.chatbot_graph.py：最终效果运行demo，输入问题得到答案。

<br>

**引用说明：**

引用了[liuhuanyong](https://github.com/liuhuanyong/QASystemOnMedicalKG)博士的一个开源项目，将爬虫部分从Request请求换成了scrapy进行爬取。当作练习scrapy。此外，对抽取了一些实体的共同点，简化了代码实现，逻辑可能更加清晰了，也更便于维护些。

