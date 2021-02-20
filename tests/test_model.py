from utils.model_helper import ModelHelper
from utils.data_helper import DataHelper


if __name__ == '__main__':
    modelHelper = ModelHelper()
    dataHelper = DataHelper()
    # content,label = dataHelper.getImdbData()
    content,label = dataHelper.getKeyWordData()

    modelHelper.tainingDataWithSVM(content,label)
    modelHelper.tainingDataWithXgboost(content,label)

    # print(modelHelper.predictBySVM("難過"))
    # modelHelper.GetCovidData()