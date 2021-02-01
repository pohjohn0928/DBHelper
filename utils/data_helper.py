import csv
import random


class DataHelper:
    def getCleanCSVData(self):
        path = "C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\20200706_rowdata.csv"
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