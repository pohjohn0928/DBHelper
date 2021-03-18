from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,accuracy_score   #,accuracy_score
from sklearn.datasets import make_multilabel_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier

from xgboost import XGBClassifier
import jieba
import joblib
import os
import abc
import numpy as np
import pickle

# from keras.models import Sequential
# from keras.layers import Dense
# import keras
from sklearn.ensemble import RandomForestClassifier

class init(abc.ABC):
    dirname = os.path.dirname(__file__)

class ModelHelper(init):
    def stopwordslist(self):
        path = os.path.join(self.dirname,'..\\text.txt')
        stopwords = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]
        return stopwords

    def tainingDataWithSVM(self,content,label):
        x_train, x_test, y_train, y_test = train_test_split(content, label, test_size=0.2, random_state=1,shuffle=True)
        vectorizer = TfidfVectorizer(max_features=5000,min_df=2,stop_words=self.stopwordslist())
        x_train_features = vectorizer.fit_transform(x_train)
        x_test_features = vectorizer.transform(x_test)

        SVCModel = svm.SVC(kernel='linear')
        SVCModel.fit(x_train_features, y_train)
        prediction_linear = SVCModel.predict(x_test_features)
        report = classification_report(y_test, prediction_linear, output_dict=True)
        print(f"SVM report : {report}")

        self.SVCModelPath = os.path.join(self.dirname,'..\\models\\svmModel.pkl')
        self.vectorizerSVMPath = os.path.join(self.dirname,'..\\models\\vectorizeSVM.pkl')
        joblib.dump(SVCModel, self.SVCModelPath)
        joblib.dump(vectorizer,self.vectorizerSVMPath)

    def tainingDataWithXgboost(self,content,label):
        x_train, x_test, y_train, y_test = train_test_split(content, label, test_size=0.2, random_state=1, shuffle=True)
        vectorizer = TfidfVectorizer(max_features=5000, min_df=2,stop_words=self.stopwordslist())
        x_train_features = vectorizer.fit_transform(x_train)
        x_test_features = vectorizer.transform(x_test)

        xgboostModel = XGBClassifier(n_estimators=100,learning_rate=0.1)
        xgboostModel.fit(x_train_features,y_train)
        predicted = xgboostModel.predict(x_test_features)
        report = classification_report(y_test,predicted,output_dict=True)
        print(f"Xgboost report {report}")

        self.xgboostModelPath = os.path.join(self.dirname,'..\\models\\xgboostModel.pkl')
        self.vectorizerXgboostPath = os.path.join(self.dirname,'..\\models\\vectorizerXgboost.pkl')
        joblib.dump(xgboostModel,self.xgboostModelPath)
        joblib.dump(vectorizer, self.vectorizerXgboostPath)

    def predictBySVM(self,str):
        str = jieba.lcut(str)
        str = " ".join(str)
        str = [str]
        vectorizer = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\vectorizeSVM.pkl")
        str = vectorizer.transform(str)
        SVCModel = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\svmModel.pkl")
        return SVCModel.predict(str)

    def predictByXgboost(self,str):
        str = jieba.lcut(str)
        str = " ".join(str)
        str = [str]
        vectorizer = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\vectorizerXgboost.pkl")
        str = vectorizer.transform(str)
        xgboostModel = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\xgboostModel.pkl")
        return xgboostModel.predict(str)

    def trainingMultiLabel(self,fact,accus):
        x_train, x_test, y_train, y_test = train_test_split(fact, accus, test_size=0.2, random_state=1, shuffle=True)
        vectorizer = TfidfVectorizer(stop_words='english',max_features=5000,min_df=2)
        x_train_features = vectorizer.fit_transform(x_train)
        x_test_features = vectorizer.transform(x_test)

        # fit
        classifier = RandomForestClassifier(random_state=1)
        # classifier = KNeighborsClassifier()
        # classifier = svm.SVC(kernel='linear')
        # classifier = XGBClassifier()

        multi_target_model = OneVsRestClassifier(classifier)
        model = multi_target_model.fit(x_train_features, y_train)
        predicted = model.predict(x_test_features)
        prob = model.predict_proba(x_test_features)
        for i in range(len(predicted)):
            print(predicted[i],prob[i])

        # for i in range(len(predicted)):
        #     print(y_test[i],predicted[i])
        print(f"accuracy_score : {accuracy_score(y_test, predicted)}")
        # eval
        right = 0
        wrong = 0
        for i in range(len(y_test)):
            for j in range(len(y_test[i])):
                if y_test[i][j] == predicted[i][j]:
                    right += 1
                else:
                    wrong += 1

        print(right / (right + wrong))

        # save
        pickle.dump(vectorizer,open("../vectorizer.pkl","wb"))
        pickle.dump(model,open("../model.pkl","wb"))

    def predictMultiLabel(self,fact):
        vectorizer = pickle.load(open("../vectorizer.pkl","rb"))
        model= pickle.load(open("../model.pkl","rb"))
        fact = jieba.lcut(fact)
        fact = " ".join(fact)
        fact = [fact]
        fact = vectorizer.transform(fact)
        results = model.predict(fact)
        prob = model.predict_proba(fact)

        print(results)
        print(prob)
        # accus_list = ["危險駕駛","故意傷害","妨礙公務","其他"]
        # accus = []
        # for result in results:
        #     in_range = 0
        #     for i in range(len(result)):
        #         if result[i] == 1:
        #             accus.append(accus_list[i])
        #             in_range = 1
        #     if in_range == 0:
        #         accus.append(accus_list[-1])
        # return accus