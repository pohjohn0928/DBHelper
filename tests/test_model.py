from utils.model_helper import ModelHelper;



if __name__ == '__main__':
    modelHelper = ModelHelper()
    content,label= modelHelper.getImdbData()
    modelHelper.tainingDataWithSVM(content,label)