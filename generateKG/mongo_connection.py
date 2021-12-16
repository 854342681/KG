import json
import os
import pymongo
import re


myclient = pymongo.MongoClient("mongodb://222.197.219.4:27017/")
mydb = myclient["db_base"]
mycol = mydb["db_lan"]
path = ['../db100k/wikidata_erro.json','../db100k/wikidata_addition.json']
insert = []
count = len(insert)
fail = []
for i in path:
    with open(i,'r',encoding='utf8') as f:
        for line in f:
            try:
                data = json.loads(line)
                insert.append(data)
            except Exception as e:
                name = re.search(r'Q\d*', line)
                try:
                    fail.append(name.group(0))
                except:
                    pass
                print(e)
        if count == 1000:
            result = mycol.insert_many(insert)
            insert = []
            print('done')
print('all done')


