import csv
import random
import os
import numpy as np
import abc
import jieba

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