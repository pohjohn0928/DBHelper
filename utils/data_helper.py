import csv
import random
import os

class DataHelper:
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
        file = open(os.path.join(dirname,f'..\\{key_word}.csv'),'w',encoding="utf-8",newline='')
        writer = csv.writer(file)
        writer.writerow(['content','label'])
        for data in row_data:
            if key_word in data[0]:
                news = data[0].replace("<BR>","").replace("\n","").replace('\r','').replace(',','.')
                writer.writerow([news])