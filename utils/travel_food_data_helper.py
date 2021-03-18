import pymysql
import csv
import numpy as np
import pandas
import random
from sklearn.utils import shuffle
from scipy.sparse import coo_matrix
import pymongo
from bson.objectid import ObjectId
from sklearn.preprocessing import MultiLabelBinarizer
import jieba

class GetData:
    def __init__(self):
        self.host = '172.18.20.190'
        self.user = "rd2"
        self.password = "eland4321"
        self.db = "forum_data"
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        self.cursor = self.conn.cursor()

    def outPutCsvFile(self):
        content = []
        label = []

        table = "ts_page_content"
        sql = f"select content from {table} where title like '%旅遊%' limit 500"
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        for data in datas:
            if data[0] in content:
                continue
            else:
                content.append(data[0])
                label.append('travel')

        sql = f"select content from {table} where title like '%美食%' limit 500"
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        for data in datas:
            if data[0] in content:
                continue
            else:
                content.append(data[0])
                label.append('food')

        sql = f"select content from {table} where title like '%廣告%' limit 500"
        self.cursor.execute(sql)
        datas = self.cursor.fetchall()
        for data in datas:
            if data[0] in content:
                continue
            else:
                content.append(data[0])
                label.append('other')


        content,label = shuffle(content,label)

        with open('../travel_food.csv', 'w', newline='',encoding='utf-8') as csvfile:
            fieldnames = ['content', 'label']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for index in range(len(content)):
                if content[index] == '':
                    continue
                else:
                    data = content[index].replace("\n","")
                    writer.writerow({'content': data, 'label': label[index]})

class GetDataFromMongo:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
        db = client.dev_index
        self.collection = db.test

    def getData(self):
        content = []
        label = []
        query = {"_id": ObjectId("6052b8a9d967f0f3d198510e")}
        cursor = self.collection.find(query, {"_id": 0, "train_file": 1})
        for i in cursor:
            for j in i["train_file"]:
                content.append(j["content"])
                label.append(j["label"])

        mlb = MultiLabelBinarizer()
        mlb.fit_transform([label])
        print(mlb.classes_)


        for i in range(len(label)):
            label[i] = mlb.transform([[label[i]]])[0]
        label = np.array(label)

        for i in range(len(content)):
            content[i] = jieba.lcut(content[i])
            content[i] = " ".join(content[i])

        return content,label

