import os
import json
import spider

if __name__ == '__main__':
    path = '../T100K/Map/fail'
    ID = []
    for file in os.listdir(path):
        print(f'正在爬取{file}的实体')
        with open(path + '/' + file, 'r') as f:
            for line in f.readlines():
                ID.append(line.strip('\n'))
    ID = list(set(ID))
    spider.main(ID, 'addition')
    print('done')