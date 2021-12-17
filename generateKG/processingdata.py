import json
import os
import random

class discriminate():
    def __call__(self, path,dfine):
        self.dfine = dfine
        wpath = path.strip('.json').split('/')[2]
        Des,Spe = self.getdic(path)
        trip_des = self.analysis(Des)
        print('稠密三元组集分析完成')
        trip_spe = self.analysis(Spe)
        print('稀疏三元组集分析完成')
        count_des = len(list(trip_des.keys()))
        count_spe = len(list(trip_spe.keys()))
        for i,j in trip_des.items():
            self.writeTXT(i,j,wpath,'des')
        print(f'{wpath} 稠密构建完成！ ')
        for i,j in trip_spe.items():
            self.writeTXT(i,j,wpath,'spe')
        print(f'{wpath} 稀疏构建完成！ ')
        return count_des,count_spe

    '''
    建立稠密、稀疏字典
    '''
    def getdic(self,path):
        data = {}
        des = {}
        spe = {}
        with open(path,'r',encoding='utf8') as f:
            data = json.load(f)
        for i,j in data.items():   #区分稠密、稀疏
            tmp_count = len(data[i])
            if self.dfine < tmp_count: #稠密
                des[i] = data[i]
            elif self.dfine > tmp_count:     #稀疏
                spe[i] = data[i]
        print('数据分析完成')
        return des,spe


    '''
    分析每个字典中的实体值
    '''
    def analysis(self,data):
        tmp = {}
        for i,j in data.items():
            for x,z in j.items():
                if x == 'labels':
                    tmp[i]={'labels':j[x]['value']}
                elif '_' in x:    #同一实体下不同尾实体相同关系的三元组组成列表形式
                    pid = x.split('_')[0]
                    if pid not in tmp[i].keys():
                        tmp[i].update({pid: [z['datavalue']['value']['id']]})
                    else:
                        tmp[i][pid].append(z['datavalue']['value']['id'])
                    tmp[i][pid] = list(set(tmp[i][pid]))  # 去除重复元素
                else:
                    tmp[i].update({x:z['datavalue']['value']['id']})
        return tmp

    def writeTXT(self,name,value,wpath,flag):
        with open(f'../T100K/trip/{wpath}_{flag}.txt','a',encoding='utf8') as f:
            for i,j in value.items():
                if i == 'labels':
                    f.write('\n' + name + ' \t' + j + ' \n')
                elif type(j) is list:
                    for x in j:
                        f.write(f'{name} \t{i} \t{x} \n')
                else:
                    f.write(f'{name} \t{i} \t{j} \n')

class generate(discriminate):
    def __call__(self, path,inti=4586,des_hop = 3,spe_hop = 3,dfine = None):
        self.dfine = dfine
        self.path = path
        self.seed = 0
        self.recount = 0
        self.wpath = path.strip('.json').split('/')[2]
        Des, Spe = self.getdic(path)  #生成文件路径
        self.KGgen(Des,'des',des_hop,inti)
        print('des done')
        self.KGgen(Spe,'spe',spe_hop,inti)
        print('spe done')


    def KGgen(self,path,flag,num,inti):
        self.recount = 0
        start = None
        temp = []  # 初始化知识图谱
        trip = self.analysis(path)  # 分析实体信息
        start = self.start(trip,inti)  # 随机抽取初始节点,获取其作为头实体的三元组
        restart = True  # 设置重启标志
        while restart:
            restart = False
            for i in start:
                temp.append(i)
            self.recount += 1
            for i in range(num):  # 扩展num跳邻居
                tmp,restart = self.getneighbour(start,trip)   # 输入上一节点三元组，以及稠密（稀疏）实体集，输出尾实体作为头实体所在的三元组集合。
                if restart:    # 如果标志位True，则重启循环。
                    print(f'restart: {self.recount}')
                    break
                for x in tmp:
                    temp.append(x)   # 加入到知识图谱中
                start = tmp    # 将新的三元组集合作为下一轮循环的初始集合
            for _ in range(1):
                if len(temp) < 15000 and self.recount < 1000:
                    print(f'restart: {self.recount}')
                    start = self.reset(trip)
                    restart = True
                    break

        self.count_and_write(temp, flag)  # 将完成的三元组集写入txt中并做统计。
        print(self.seed)

    def reset(self,trip):   # 重置初始节点
        self.seed = random.randint(0,100000)  # 随机选择种子（即：重新随机选初始节点）
        return  self.start(trip,self.seed)

    def start(self,trip,seed):
        tmp = []
        random.seed(seed)
        start = random.sample(trip.keys(),1)[0]
        pro = trip[start]
        try:
            del pro['labels']
        except:
            pass
        for i,j in pro.items():
            if type(j) is list:
                for x in j:
                    tmp.append([start, i, x])
            else:
                tmp.append([start,i,j])
        return tmp

    def getneighbour(self,start,trip):
        tmp = []
        temp = []
        for i in start:
            i = i[2]
            if i in trip:
                tmp.append(i)
        if tmp is None:    # 判断初始实体集是否有在实体集中的三元组，如果没有则重启循环。
            return self.reset(trip),True
        for x in tmp:
            value = trip[x]
            try:                     # 删除'labels'字典
                del value['labels']
            except:
                pass
            for h,j in value.items():  #  遍历剩下的 h=关系 ('Pxxx')  i=尾实体 ('Qxxxxx')
                if type(j) is list:    #  如果同一关系下有多个尾实体，分别给出其三元组
                    for m in j:
                        temp.append([x, h, m])
                else:
                    temp.append([x, h, j])
        return temp,False

    def count_and_write(self,kg,flag):
        if os.path.exists(f'../T100K/KG/{flag}') is False:
            os.makedirs(f'../T100K/KG/{flag}')
        count = len(kg)
        with open(f'../T100K/KG/{flag}/{self.wpath}.txt','a',encoding='utf8') as f:
            for i in kg:
                f.write(i[0] + ' \t' + i[1] + ' \t' + i[2] + ' \n')
        with open(f'../T100K/KG/{flag}/count.txt','a',encoding='utf8') as f:
            f.write(self.wpath + '\t' + str(count) + '\n')

class mapping():
    def __call__(self, path):
        self.wpath = path
        self.path = f'../T100K/{path}'
        self.index = {}
        self.dataset()
        self.entity_map()
        self.writeJSON()
    def dataset(self):
        with open(self.path,'r',encoding='utf8') as f:
            self.data = json.load(f)
    def entity_map(self):
        for i,j in self.data.items():
            name = j['labels']['value']
            lang = (j['labels']['language'])
            self.index[i] = name
    def writeJSON(self):
        with open(f'../T100K/Map/{self.wpath}','w',encoding='utf8') as f:
            json.dump(self.index,f)
        print(f'完成{self.wpath}的写入')


def Printtrip(path,num):
    a = discriminate()
    for i in path:
        if '.json' and '_rel' in i:
            descount,specount = a(f'../T100K/{i}',num[i])
            with open('../T100K/trip/count.txt','a',encoding='utf8') as f:
                f.write(f'{i} \tdes:{descount} \tspe:{specount} \n')
            print(f'-----------------{i} 所有三元组构建完毕！-------------------------\n')


def PrintKG(path,seed,num):
    b = generate()
    for i in path:
        if '.json' and '_rel' in i and i in seed:
            if seed[i]['seed'] is None:
                b(f'../T100K/{i}',des_hop=seed[i]['des_hop'],spe_hop=seed[i]['spe_hop'],dfine=num[i])
            else:
                b(f'../T100K/{i}',seed[i]['seed'],des_hop=seed[i]['des_hop'],spe_hop=seed[i]['spe_hop'],dfine=num[i])
            print(f'-------------------------------------{i} is done!-------------------------------------')

def GetMap(path):
    c = mapping()
    for i in path:
        if '.json' and '_rel' in i:
            c(i)

if __name__ == '__main__':
    seed = {'en_rel.json':{'seed':6709,'des_hop':3,'spe_hop':11},
            'lo_rel.json':{'seed':50208,'des_hop':3,'spe_hop':8},
            'my_rel.json':{'seed':28560,'des_hop':3,'spe_hop':6},
            'th_rel.json':{'seed':73165,'des_hop':2,'spe_hop':8},
            'vi_rel.json':{'seed':74390,'des_hop':3,'spe_hop':10},
            'zh_rel.json':{'seed':54885,'des_hop':3,'spe_hop':10}}   # 记录正确的初始种子
    define = {'en_rel.json':9,
            'lo_rel.json':20,
            'my_rel.json':20,
            'th_rel.json':18,
            'vi_rel.json':13,
            'zh_rel.json':13}
    path = os.listdir('../T100K')
    if os.path.exists('../T100K/trip') is False:
        os.makedirs('../T100K/trip')
    if os.path.exists('../T100K/KG') is False:
        os.makedirs('../T100K/KG')
    # GetMap(path)
    # Printtrip(path,define)
    # print('\n稀疏、稠密三元组集构建完成\n')
    PrintKG(path,seed,define)
    print('\n稀疏、稠密知识图谱构建完成\n')



