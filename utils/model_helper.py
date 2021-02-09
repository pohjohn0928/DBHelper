from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import jieba
import joblib

class ModelHelper:
    def getImdbData(self):
        path = "C:\\Users\\taisiangbo\\Desktop\\sentimentalDataset.txt"
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
                    content = jieba.lcut(content)
                    content = ''.join(content)
                    contents.append(content)
                    labels.append(label)
                if label == "正面":
                    positive += 1
                    content = word[:-3]
                    content = jieba.lcut(content)
                    content = ''.join(content)
                    contents.append(content)
                    labels.append(label)
            except:
                continue
        f.close()
        return contents,labels

    def stopwordslist(self):
        filepath = "C:\\Users\\taisiangbo\\Desktop\\text.txt"
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def tainingDataWithSVM(self,content,label):
        x_train, x_test, y_train, y_test = train_test_split(content, label, test_size=0.2, random_state=1,shuffle=True)
        vectorizer = TfidfVectorizer(stop_words=self.stopwordslist())
        x_train_features = vectorizer.fit_transform(x_train)
        x_test_features = vectorizer.transform(x_test)
        SVCModel = svm.SVC(kernel='linear')
        SVCModel.fit(x_train_features, y_train)
        prediction_linear = SVCModel.predict(x_test_features)
        report = classification_report(y_test, prediction_linear, output_dict=True)
        print(f"SVM report : {report}")
        joblib.dump(SVCModel, 'C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\svmModel.pkl')
        joblib.dump(vectorizer,'C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\vectorizeSVM.pkl')

    def tainingDataWithXgboost(self,content,label):
        x_train, x_test, y_train, y_test = train_test_split(content, label, test_size=0.2, random_state=1, shuffle=True)
        vectorizer = TfidfVectorizer(stop_words=self.stopwordslist())
        x_train_features = vectorizer.fit_transform(x_train)
        x_test_features = vectorizer.transform(x_test)

        xgboostModel = XGBClassifier(n_estimators=100,learning_rate=0.1)
        xgboostModel.fit(x_train_features,y_train)
        predicted = xgboostModel.predict(x_test_features)
        report = classification_report(y_test,predicted,output_dict=True)
        print(f"Xgboost report {report}")
        joblib.dump(xgboostModel,'C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\xgboostModel.pkl')
        joblib.dump(vectorizer, 'C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\vectorizerXgboost.pkl')

    def predictBySVM(self,str):
        str = [str]
        vectorizer = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\vectorizeSVM.pkl")
        str = vectorizer.transform(str)
        SVCModel = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\svmModel.pkl")
        return SVCModel.predict(str)

    def predictByXgboost(self,str):
        str = [str]
        vectorizer = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\vectorizerXgboost.pkl")
        str = vectorizer.transform(str)
        xgboostModel = joblib.load("C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\models\\xgboostModel.pkl")
        return xgboostModel.predict(str)

