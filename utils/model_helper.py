from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import jieba
import joblib
import os
import abc

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

