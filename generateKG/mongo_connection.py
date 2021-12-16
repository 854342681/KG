import json
import os
import pymongo
import re

'''
连接数据库，创建collection
'''
myclient = pymongo.MongoClient("mongodb://222.197.219.4:27017/")
mydb = myclient["db_base"]
mycol = mydb["db_lan"]

path = ['../db100k/wikidata_erro.json','../db100k/wikidata_addition.json']
insert = []   # 输入数据的集合
count = len(insert)   # 计数
fail = []   # 失败数据集合
for i in path:
    with open(i,'r',encoding='utf8') as f:
        for line in f:  # 文件过大，只能逐行打开文件
            try:
                data = json.loads(line)
                insert.append(data)
            except Exception as e:  # 如果出错，则找到Qid，记录下来。如没有Qid就直接舍弃这段数据
                name = re.search(r'Q\d*', line)
                try:
                    fail.append(name.group(0))
                except:
                    pass
                print(e)
        if count == 1000:   # 性能原因无法在内存中存储过多的数据，每存1000个上传一次并清空集合
            result = mycol.insert_many(insert)
            insert = []
            print('done')
print('all done')


