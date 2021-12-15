import json
import os
import tqdm

'''
映射实体ID和实体名称
输入：
    三元组集（TXT文件）路径   如：'../T100K/KG/des/en_rel.txt'
    映射关系集（JSON文件）路径   如：'../T100K/Map/en_rel.json'
输出：
    映射好的三元组列表(list)   如： [['Trzebnica County', 'P47', 'Wołów County'], ['Trzebnica County', 'P47', 'Milicz County']]
    无映射ID表，在'../T100K/Map/fail'文件夹下
'''
class map_en_name():
    def __call__(self,en_path,map_path):
        self.map_path = map_path
        self.en_path = en_path
        map_data = self.readJSON(self.map_path)  # 读取JSON   map_data(dict) =  {'Q4712436': 'Șimon River', 'Q865639': 'Șoldănești District', 'Q4711738': 'Șușița River', 'Q3291734': 'Șușița River', 'Q213984': 'חרה', 'Q3596267': '’Til Tuesday'}
        print('JSON读取完毕')
        en_data = self.readTXT(self.en_path)  # 读取TXT
        print('TXT读取完毕')
        en_data = self.procTXT(en_data)      # 解析读取的TXT数据   en_data(list) = [['Q715630', 'P47', 'Q1799'], ['Q715630', 'P47', 'Q657314'], ['Q715630', 'P47', 'Q715925'], ['Q715630', 'P47', 'Q715413']]
        print('TXT分析完毕')
        return  self.map(map_data,en_data)   # 返回映射好的列表作为输出

    def readJSON(self,path):
        with open(path,'r',encoding='utf8') as f:
            return json.load(f)

    def readTXT(self,path):
        with open(path,'r',encoding='utf8') as f:
            data = []
            for line in f:                    # 避免TXT过大，选择逐行读取文件
                data.append(line)
        return data

    def procTXT(self,data):                   # 根据TXT格式变换处理流程
        temp = []
        for i in data:
            tmp = []
            i = i.strip(' \n').split(' \t')
            for x in i:
                tmp.append(x)
            temp.append(tmp)
        return temp

    def map(self,md,ed):  #
        result = []
        wpath = self.en_path.split('/')[-1]
        fail = []
        for i in ed:                            # 提取出三元组   ['Q715630', 'P47', 'Q1799']
            tmp = []
            for x in i:                         # 遍历三元组中的每个元素进行映射
                if x in md:                     # 如果映射集中有则替换
                    tmp.append(md[x])
                elif x not in md and 'Q' in x:  # 如果是Q实体，但是映射集中没有映射，则输出本身，并且记录成TXT
                    tmp.append(x)
                    fail.append(x)
                else:                           # 剩下的为P关系，输出本身
                    tmp.append(x)
            result.append(tmp)
        fail = list(set(fail))
        for i in fail:
            with open(f'../T100K/Map/fail/{wpath}', 'a') as f:
                f.write(i + '\n')
        print('映射完毕')
        return result

if __name__ == '__main__':
    map_dir = '../T100K/Map'
    en_dir = '../T100K/KG'
    final_trip = {}
    a = map_en_name()
    map_list = os.listdir(map_dir)
    en_list = os.listdir(en_dir)
    del map_list[map_list.index('fail')]
    for i in en_list:
        tmp = os.listdir(f'{en_dir}/{i}')
        del tmp[tmp.index('count.txt')]
        for x,z in zip(tmp,map_list):
            en_path = en_dir + '/' + i + '/' + x
            map_path = map_dir + '/' + z
            temp = a(en_path,map_path)
            final_trip[x] = temp
            print(f'{x}到{z}的实体名称映射完毕')
    with open('../T100K/KG/mapping.json','w',encoding='utf8') as f:
        json.dump(final_trip,f)
    print('done')