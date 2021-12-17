# coding=utf-8
import requests
import threading
from queue import Queue
import json
import os
import QQmail as qq

#生产者：爬取网页信息保存进内容队列（content_queue）
class Producter(threading.Thread):
    def __init__(self,id_queue,content_queue,*args,**kwargs):
        super(Producter,self).__init__(*args,**kwargs)
        self.id_queue = id_queue
        self.content_queue = content_queue

    def run(self):
        while True:
            if self.id_queue.empty():
                print('读取完成')
                break
            else:
                idx = self.id_queue.get()
                self.page(idx)



    def page(self,idx):
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{idx}.json"
        pox = {"http": "http://127.0.0.1:7980", "https": "http://127.0.0.1:7980"}
        try:
            html = requests.get(url, proxies=pox, timeout=5).text
            html = json.loads(html)['entities'][f'{idx}']
            self.content_queue.put(html)
            print('读取成功')
        except Exception as e:
            with open('../db100k/erro_1.txt','a') as f:      #一般失败的是请求过于频繁造成的无响应，保存进额外的文件中以便之后重新爬取
                f.write(idx + '\n')
            print(f'{idx}获取错误',e)


# 消费者：从内容队列中取出内容写入对应文件中
class Coumser(threading.Thread):
    def __init__(self,id_queue,content_queue,num,*args,**kwargs):
        super(Coumser,self).__init__(*args,**kwargs)
        self.id_queue = id_queue
        self.content_queue = content_queue
        self.filename = f'../db100k/wikidata_{num}.json'

    def run(self):
        while True:
            if self.content_queue.empty() and self.id_queue.empty():
                print('写入完成')
                break
            else:
                L = self.content_queue.get()
                idx = L['id']
                self.writeJSON(L,idx)
                self.content_queue.task_done()



    def writeJSON(self,L,idx):
        try:
            with open(self.filename,'a',encoding='utf8') as f:
                L = json.dumps(L)
                f.write(L+'\n')
                print('写入成功')
        except Exception as e:
            print(f'{idx}写入失败，错误为：    ',e)

id_queue = Queue(200000)   #队列最大数量应大于数据数
content_queue = Queue(10000)
def main(index,num):
    for x in index:
        id_queue.put(x)

    pro_thread = []
    cou_thread = []
    #写入线程并启动
    for x in range(20):
        t = Producter(id_queue, content_queue)
        t.start()
        pro_thread.append(t)

    for x in range(10):
        t = Coumser(id_queue, content_queue,num)
        t.start()
        cou_thread.append(t)
    #等待所有线程执行完毕
    for x in pro_thread:
        x.join()

    for x in cou_thread:
        x.join()

if __name__ == '__main__':
    path = './ID'
    '''
    从ID文件夹中逐一读取文件，并根据文件ID爬取信息,
    （ID为事先将所需爬取的139万个数据以1万大小分块存储进行爬取，以防爬取后保存的文件过大读取处理时占用过多的时间甚至无法打开）
    '''
    for file in os.listdir(path):
        print(f'正在爬取{file}的实体')
        num = os.path.splitext(file)[0]
        try:
            with open(path +'/' + file,'r') as f:
                ID = []
                for line in f.readlines():
                    ID.append(line.strip('\n'))
                main(ID,num)
                print(f'完成{file}的数据爬取，爬取{len(ID)}个实体，保存在"wikidata_{num}.json"文件中')
        except Exception:
            print(f'无{file}文件')
    print('完成实体爬取任务')




