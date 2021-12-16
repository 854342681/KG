import json
import pymongo
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
            json.dump(r, f)

        with open(f'{self.path}/{lang}_attr.json', 'w', encoding='utf8') as f:
            json.dump(a, f)


    def getValue(self,tmp_rel,tmp_attr,tmp,i,j,dic_path):
        try:
            datavalue = tmp['mainsnak']['datavalue']
            if datavalue['type'] == 'wikibase-entityid':  #有关系时记录为‘关系’
                tmp_rel[j['title']][dic_path] = {'datavalue': datavalue}
            else:
                tmp_attr[j['title']][dic_path] = {'datavalue': datavalue} #其余记录为‘属性’
        except Exception as e:
            print(f'{j["title"]}   {i}  错误:  ', e)

    '''
    tmp_rel:
            "Q371": {
                "labels": [
                    {
                        "language": "zh",
                        "value": "!!!"
                    },
                    {
                        "language": "th",
                        "value": "!!!"
                    }
                ],
                "P136_0": {
                    "datavalue": {
                        "value": {
                            "entity-type": "item",
                            "numeric-id": 1643549,
                            "id": "Q1643549"
                        },
                        "type": "wikibase-entityid"
                    }
                }
        
        tmp_attr:
                "Q371": {
                "labels": [
                    {
                        "language": "zh",
                        "value": "!!!"
                    },
                    {
                        "language": "th",
                        "value": "!!!"
                    }
                ],
                "P244": {
                    "attribute": {
                        "value": "no2005023261",
                        "type": "string"
                    }
                }
    '''
    def getContext(self,doc,x):
        tmp_rel = {}
        tmp_attr = {}
        for j in doc:
            lang = j['labels'][x]
            tmp_rel[j['title']] = {'labels': lang}
            tmp_attr[j['title']] = {'labels': lang}
            claims = j['claims']
            relation = list(claims.keys()) # 关系集合
            for i in relation: # 遍历关系集，如果有重复的则以’_0‘、’_1‘…………结尾作标注。
                if len(claims[i]) > 1:
                    for m in range(len(claims[i])):
                        tmp = claims[i][m]
                        self.getValue(tmp_rel,tmp_attr,tmp,i,j,f'{i}_{m}')
                else:
                    tmp = claims[i][0]
                    self.getValue(tmp_rel,tmp_attr,tmp,i,j,i)
        self.writeJSON(x,tmp_rel,tmp_attr)

'''
获取种子（两个语言都有的实体为种子）
'''
class makeSeed():
    def __init__(self, col, rel: dict, attr: dict, language: list, path):
        self.searchlang = [language[0],language[1]]
        del language[0]
        del language[0]
        self.mycol = col
        self.rel = rel
        self.attr = attr
        self.language = language
        self.path = path


    def __call__(self):
        for i in self.searchlang:
            for j in self.language:
                doc = mycol.find({"$and": [{f"labels.{i}": {"$exists": True}},{f"labels.{j}": {"$exists": True}}]}).limit(500)
                self.getContext(doc, i,j)
        print('-' * 20, ' Done! ', '-' * 20)

    def writeJSON(self, search,target, r, a):
        with open(f'{self.path}/{search}_{target}_rel.json', 'w', encoding='utf8') as f:
            json.dump(r, f)

        with open(f'{self.path}/{search}_{target}_attr.json', 'w', encoding='utf8') as f:
            json.dump(a, f)

    def getContext(self,doc,search,target):
        tmp_rel = {}
        tmp_attr = {}
        for j in doc:
            lang = [j['labels'][search],j['labels'][target]]
            tmp_rel[j['title']] = {'labels': lang}
            tmp_attr[j['title']] = {'labels': lang}
            claims = j['claims']
            relation = list(claims.keys()) # 关系集合
            for i in relation: # 遍历关系集，如果有重复的则以’_0‘、’_1‘…………结尾作标注。
                if len(claims[i]) > 1:
                    for m in range(len(claims[i])):
                        tmp = claims[i][m]
                        self.getValue(tmp_rel,tmp_attr,tmp,i,j,f'{i}_{m}')
                else:
                    tmp = claims[i][0]
                    self.getValue(tmp_rel,tmp_attr,tmp,i,j,i)
        self.writeJSON(search,target,tmp_rel,tmp_attr)

    def getValue(self,tmp_rel,tmp_attr,tmp,i,j,dic_path):
        try:
            datavalue = tmp['mainsnak']['datavalue']
            if datavalue['type'] == 'wikibase-entityid':  #有关系时记录为‘关系’
                tmp_rel[j['title']][dic_path] = {'datavalue': datavalue}
            else:
                tmp_attr[j['title']][dic_path] = {'datavalue': datavalue} #其余记录为‘属性’
        except Exception as e:
            print(f'{j["title"]}   {i}  错误:  ', e)



myclient = pymongo.MongoClient("mongodb://222.197.219.4:27017/")
mydb = myclient["db_base"]
mycol = mydb["db_lan"]

# 修改语言  my vi lo 等查询语言
rel = {}
attr = {}
language = ['zh','en','my','vi','lo','th']
t = getJSON(mycol,rel,attr,language,'../T100k/')
t()
e = makeSeed(mycol,rel,attr,language,'../T100k/seed')
e()
mail = QQmail.Mail('854342681@qq.com','2221078665@qq.com','tjf','完成','快回来！')
mail.send()

