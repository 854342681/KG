import os

import spider

if __name__ == '__main__':
    path = '../T100K/Map/fail'
    for file in os.listdir(path):
        print(f'正在爬取{file}的实体')
        name = os.path.splitext(file)[0]
        try:
            with open(path + '/' + file, 'r') as f:
                ID = []
                for line in f.readlines():
                    ID.append(line.strip('\n'))
                spider.main(ID, name)
                print(f'完成{file}的数据爬取，爬取{len(ID)}个实体，保存在"wikidata_{file}.json"文件中')
        except Exception:
            print(f'无{file}文件')