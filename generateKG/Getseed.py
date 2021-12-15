import os
import json

'''
获取种子三元组
输入：
    种子json所在的文件夹
    种子json文件名（带扩展符）
输出：
    提取好的种子三元组json文件
'''
class Getseed():
    def __init__(self,dir):
        self.path = dir

    def __call__(self,path):
        self.path = dir + '/' + path
        self.wpath = f'../T100K/seedtrip/{path.split(".")[0]}.txt'
        data = self.readData()
        trip = self.getTrip(data)
        self.write(trip)

    def readData(self):
        with open(self.path,'r',encoding='utf8') as f:
            data = json.load(f)
        print(f'{self.path} readed !')
        return data

    def getTrip(self,data):
        heads = list(data.keys())
        tmp = []
        for i in heads:
            pro = data[i]
            del pro['labels']
            for x,z in pro.items():
                if '_' in x:
                    x = x.split('_')[0]
                    tmp.append([i,x,z['datavalue']['value']['id']])
                else:
                    tmp.append([i,x,z['datavalue']['value']['id']])
        print(f'{self.path} trip get !')
        return tmp

    def write(self,trip):
        with open(self.wpath,'a',encoding='utf8') as f:
            for i in trip:
                f.write(f'{i[0]} \t{i[1]} \t{i[2]} \n')
        print(f'{self.wpath} wrote !')

if __name__ == '__main__':
    dir = '../T100K/seed'
    path = os.listdir(dir)
    a = Getseed(dir)
    for i in path:
        a(i)
    print('Done!')