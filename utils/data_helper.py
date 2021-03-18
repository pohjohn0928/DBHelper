import csv
import random
import os
import numpy as np
import abc
import jieba
import json
from opencc import OpenCC

class init(abc.ABC):
    dirname = os.path.dirname(__file__)

class DataHelper(init):
    def getCleanCSVData(self):
        path = "..\\20200706_rowdata.csv"
        raw_data = []
        f = open(path, encoding='utf-8')
        rows = csv.reader(f)
        for row in rows:
            news = row[0].replace("'", "\\'")  # 跳脫字元
            if len(news) < 10000:
                raw_data.append(news)
        f.close()
        random.shuffle(raw_data)
        return raw_data

    def dataToCSV(self,row_data,key_word):
        dirname = os.path.dirname(__file__)
        row_data = set(row_data)
        file = open(os.path.join(dirname,f'..\\{key_word}.csv'),'w',encoding="utf-8",newline='')
        writer = csv.writer(file)
        writer.writerow(['id','content','Task Id','label'])
        result = []
        for data in row_data:
            if key_word in data[0]:
                news = data[0].replace("<BR>","").replace("\n","").replace('\r','').replace(',','.')
                new = news.split("。")
                if key_word in new[0]:
                    result.append(new[0])
        result = set(result)
        for i in result:
            writer.writerow(['', i, '', ''])

    def getImdbData(self):
        path = os.path.join(self.dirname,'..\\sentimentalDataset.txt')
        f = open(path,encoding='utf-8',mode="r")
        words = f.read()
        words = words.split("\n")
        contents = []
        labels = []
        negtive = 0
        positive = 0
        for word in words:
            try:
                label = word[-2] + word[-1]
                if label == "負面":
                    content = word[:-3]
                    negtive += 1
                    content = np.array(jieba.lcut(content))
                    content = " ".join(content)
                    contents.append(content)
                    labels.append(label)
                if label == "正面":
                    positive += 1
                    content = word[:-3]
                    content = np.array(jieba.lcut(content))
                    content = " ".join(content)
                    contents.append(content)
                    labels.append(label)
            except:
                continue
        print(f"positive data : {positive}筆")
        print(f"negative data : {negtive}筆")
        f.close()
        return np.array(contents),np.array(labels)

    def getKeyWordData(self):
        path = "..\\download.csv"
        f = open(path, encoding='cp950')
        contents = []
        labels = []
        positive = 0
        positiveNews = []
        negative = 0
        negativeNews = []
        rows = csv.reader(f)
        for row in rows:
            if row[-1] == "negative":
                negative += 1
                content = jieba.lcut(row[1])
                content = " ".join(content)
                negativeNews.append(content)

            if row[-1] == "positive":
                positive += 1
                content = jieba.lcut(row[1])
                content = " ".join(content)
                positiveNews.append(content)
        for item in positiveNews[0:min(positive,negative)]:
            contents.append(item)
            labels.append("正面")
        for item in negativeNews[0:min(positive,negative)]:
            contents.append(item)
            labels.append("負面")
        print(f"positive data : {positive}筆")
        print(f"negative data : {negative}筆")
        f.close()
        return np.array(contents), np.array(labels)


    def getMultipleLabelsData(self):
        file = open("C:\\Users\\taisiangbo\\Downloads\\CAIL2018_ALL_DATA\\final_all_data\\exercise_contest\\data_train.json","r",encoding='utf-8')
        cc = OpenCC('s2hk')

        fact = []
        accus = []
        limit = 150
        dan_drive = 0   # [1,0,0]
        harm = 0        # [0,1,0]
        off_duty = 0    # [0,0,1]
        dri_harm = 0    # [1,1,0]
        dri_off = 0     # [1,0,1]
        harm_off = 0    # [0,1,1]
        others = 0      # [0,0,0]
        for line in file.readlines():
            if [harm,dri_harm,off_duty,dri_off,harm_off,dri_harm,others] == [limit] * 7:
                break
            dic = json.loads(line)
            labels = dic["meta"]["accusation"]
            label = ",".join(labels)
            label = cc.convert(label)

            content = dic["fact"]
            if label == '故意傷害' and harm < limit:
                harm += 1
                fact.append(content)
                accus.append([0,1,0])
            elif label == '危險駕駛' and dan_drive < limit:
                dan_drive += 1
                fact.append(content)
                accus.append([1,0,0])
            elif label == '妨害公務' and off_duty < limit:
                off_duty += 1
                fact.append(content)
                accus.append([0,0,1])
            elif label == '危險駕駛,故意傷害' and dri_harm < limit:
                dri_harm += 1
                fact.append(content)
                accus.append([1,1,0])
            elif label == '故意傷害,妨害公務' and harm_off < limit:
                harm_off += 1
                fact.append(content)
                accus.append([0,1,1])
            elif label == '危險駕駛,妨害公務' and dri_off < limit:
                dri_off += 1
                fact.append(content)
                accus.append([1,0,1])
            elif others < limit:
                others += 1
                fact.append(content)
                accus.append([0,0,0])

        for i in range(len(fact)):
            content = cc.convert(fact[i])
            content = jieba.lcut(content)
            content = " ".join(content)
            fact[i] = content
        return fact,accus

