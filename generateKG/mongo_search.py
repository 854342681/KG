import json

import pymongo
import time
import tqdm
import QQmail

'''
获取JSON
'''
class getJSON():
    def __init__(self,col,rel:dict,attr:dict,language:list,path):
        self.mycol = col
        self.rel = rel
        self.attr = attr
        self.language = language
        self.path = path

    def __call__(self):
        for i in self.language:
            doc = mycol.find({f"labels.{i}": {"$exists": True}}).limit(100000)
            self.getContext(doc,i)

        print('-'*20,' Done! ','-'*20)

    def writeJSON(self,lang,r,a):
        with open(f'{self.path}/{lang}_rel.json', 'w', encoding='utf8') as f:
            # for i,j in r:
            #     tmp = {i:j}
            json.dump(r, f)
            #     f.write('\n')

        with open(f'{self.path}/{lang}_attr.json', 'w', encoding='utf8') as f:
            # for i, j in a:
            #     tmp = {i: j}
            json.dump(a, f)
            #     f.write('\n')

    def getValue(self,tmp_rel,tmp_attr,tmp,i,j,dic_path):
        try:
            datavalue = tmp['mainsnak']['datavalue']
            if datavalue['type'] == 'wikibase-entityid':  #有关系时记录为‘关系’
                tmp_rel[j['title']][dic_path] = {'datavalue': datavalue}
            else:
                tmp_attr[j['title']][dic_path] = {'attribute': datavalue} #其余记录为‘属性’
        except Exception as e:
            print(f'{j["title"]}   {i}  错误:  ', e)

    def getContext(self,doc,search):
        tmp_rel = {}
        tmp_attr = {}
        for j in doc:
            lang = j['labels'][search]
            tmp_rel[j['title']] = {'labels': lang}
            tmp_attr[j['title']] = {'labels': lang}
            claims = j['claims']
            relation = list(claims.keys())
            for i in relation:
                if len(claims[i]) > 1:
                    for m in range(len(claims[i])):
                        tmp = claims[i][m]
                        self.getValue(tmp_rel,tmp_attr,tmp,i,j,f'{i}_{m}')
                else:
                    tmp = claims[i][0]
                    self.getValue(tmp_rel,tmp_attr,tmp,i,j,i)
        self.writeJSON(search,tmp_rel,tmp_attr)





myclient = pymongo.MongoClient("mongodb://222.197.219.4:27017/")
mydb = myclient["db_base"]
mycol = mydb["db_lan"]

# 修改语言  my vi lo 等查询语言
rel = {}
attr = {}
language = ['zh','en','my','vi','lo','th']
# with open('./db100k/zh_th_rel.json','r',encoding='utf8') as f:
#     data = json.load(f)

t = getJSON(mycol,rel,attr,language,'./T100k/addition')
t()
mail = QQmail.Mail('854342681@qq.com','2221078665@qq.com','tjf','完成','快回来！')
mail.send()
1111
