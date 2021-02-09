from utils.model_helper import ModelHelper;
import jieba

if __name__ == '__main__':
    modelHelper = ModelHelper()
    content,label = modelHelper.getImdbData()
    # modelHelper.tainingDataWithSVM(content,label)
    # modelHelper.tainingDataWithXgboost(content,label)
    # print(modelHelper.predictBySVM("難過"))