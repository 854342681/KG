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

'''
读取文件，导入数据
'''
path = ['../db100k/wikidata_erro.json','../db100k/wikidata_addition.json']
insert = []   # 输入数据的集合
fail = []   # 失败数据集合
faildata = []
for i in path:
    with open(i,'r',encoding='utf8') as f:
        for line in f:  # 文件过大，只能逐行打开文件
            try:
                data = json.loads(line)
                insert.append(data)
            except Exception as e:  # 如果出错，则找到Qid，记录下来。如没有Qid就直接舍弃这段数据
                name = re.search(r'Q\d*', line)
                try:
                    faildata.append(line)
                    fail.append(name.group(0))
                except:
                    pass
                print(e)
            if len(insert) == 100:   # 性能原因无法在内存中存储过多的数据，每存1000个上传一次并清空集合
                result = mycol.insert_many(insert)
                insert = []
                with open('../db100k/fail.json', 'w', encoding='utf8') as f:
                    json.dump(faildata, f)
                    faildata = []
                print('done')
with open('../db100k/fail.txt','w',encoding='utf8') as f:
    for i in fail:
        f.write(i + '\n')
print('all done')


