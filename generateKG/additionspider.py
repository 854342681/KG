import os
import json
import spider

class analysis():
    def __init__(self,language):
        self.lang = language
        self.output = {}

    def __call__(self,path):
        self.data = []
        self.path = path
        self.read()

    def read(self):
        with open(self.path,'r',encoding='utf8') as f:
            for line in f:
                try:
                    line = json.loads(line)
                    entity = line['title']
                    self.jugdment(line)
                    print(f'\n{entity}判断完毕\n')
                except Exception as e:
                    print(e)

    def jugdment(self,data:dict):
        for i in self.lang:
            try:
                if list(data['labels'].keys()).count(i) > 0:
                    tmp_rel = {}
                    tmp_attr = {}
                    id = data['title']
                    name = data['labels'][i]
                    claims = data['claims']
                    tmp_rel[id] = {'labels':name}
                    tmp_attr[id] = {'labels':name}
                    r,a = self.getpro(claims,tmp_rel,tmp_attr,id)
                    self.writeJSON(i,r,a)
            except Exception as e:
                print(i,'\t',e)

    def getpro(self,claims,tmp_rel,tmp_attr,id):
        relation = list(claims.keys())
        for i in relation:
            try:
                tmp_value = claims[i][0]['mainsnak']['datavalue']
                if tmp_value['type'] == 'wikibase-entityid':
                    tmp_rel[id].update({i:{'datavalue':tmp_value}})
                else:
                    tmp_attr[id].update({i:{'attribute':tmp_value}})
            except Exception as e:
                print(i,'\t',e)
        return tmp_rel,tmp_attr

    def writeJSON(self, lang, r, a):
        with open(f'../T100K/{lang}_rel.json', 'a', encoding='utf8') as f:
            json.dump(r, f)

        with open(f'../T100K/{lang}_attr.json', 'a', encoding='utf8') as f:
            json.dump(a, f)



if __name__ == '__main__':
    path = '../T100K/Map/fail'
    ID = []

    # for file in os.listdir(path):
    #     print(f'正在爬取{file}的实体')
    #     with open(path + '/' + file, 'r') as f:
    #         for line in f.readlines():
    #             ID.append(line.strip('\n'))
    # with open('../db100k/erro.txt','r',encoding='utf8') as f:
    #     for line in f:
    #         line = line.strip('\n')
    #         ID.append(line)
    # ID = list(set(ID))
    # spider.main(ID, 'erro')
    language = ['zh','en','my','vi','lo','th']
    a = analysis(language)
    d = ['../db100k/wikidata_erro.json','../db100k/wikidata_addition.json']
    for i in d:
        a(i)
    print('done')