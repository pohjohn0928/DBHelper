import csv
import numpy as np
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class ModelHelper:
    def getImdbData(self):
        path = "C:\\Users\\taisiangbo\Downloads\\archive\\IMDB_Dataset.csv"
        content = []
        label = []
        f = open(path, encoding='utf-8')
        negative = 0
        positive = 0
        rows = csv.reader(f)
        counter = 0
        for row in rows:
            row[0] = row[0].replace("<br />", "")
            content.append(row[0])
            label.append(row[1])
            if row[1]=='positive':
                positive += 1
            if row[1] == 'negative':
                negative += 1

            counter += 1
            if counter > 2000:
                break
        print(f"positive review : {positive}")
        print(f"negative review : {negative}")
        del content[0]
        del label[0]
        content = np.array(content)
        label = np.array(label)
        return content,label

    def tainingDataWithSVM(self,content,label):
        x_train, x_test, y_train, y_test = train_test_split(content, label, test_size=0.2, random_state=1,shuffle=True)
        vectorizer = TfidfVectorizer(max_features=5000,min_df=5,max_df=0.8)
        x_train_features = vectorizer.fit_transform(x_train)
        x_test_features = vectorizer.transform(x_test)

        classifier_linear = svm.SVC(kernel='linear')
        classifier_linear.fit(x_train_features, y_train)
        prediction_linear = classifier_linear.predict(x_test_features)

        report = classification_report(y_test, prediction_linear, output_dict=True)
        print(report)