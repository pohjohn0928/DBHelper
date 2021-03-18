# -*- coding: utf-8 -*-
from utils.model_helper import ModelHelper
from utils.data_helper import DataHelper
from utils.travel_food_data_helper import GetDataFromMongo

if __name__ == '__main__':
    modelHelper = ModelHelper()
    dataHelper = DataHelper()
    # content,label = dataHelper.getImdbData()
    # print(content)
    # print(label)
    # print(content)
    # content,label = dataHelper.getKeyWordData()
    # print(len(content))
    # print(len(label))
    # modelHelper.tainingDataWithSVM(content,label)
    # modelHelper.tainingDataWithXgboost(content,label)

    # print(modelHelper.predictBySVM("難過"))
    # modelHelper.GetCovidData()

    # modelHelper.getMultipleLabelsData()

    # fact,accus = dataHelper.getMultipleLabelsData()
    # for i in range(len(fact)):
    #     print(fact[i],accus[i])

    getDataFromMongo = GetDataFromMongo()
    content,label = getDataFromMongo.getData()

    # modelHelper.trainingMultiLabel(content,label)
    modelHelper.predictMultiLabel("美食好吃小龍蝦旅遊")



    # predict_fact = "桂林市叠彩区人民检察院指控：2010年9月24日20时30分许，被告人何X峰（已判刑）为泄私愤，雇佣被告人谢某（已判刑）从柳州带领李X贵（已判刑）、董X龙（另案处理）、李X红（在逃）、被告人李3某到平乐县XX镇XX街X号被害人莫某乙的家门前，由何某、谢某、李1某接应，被告人李3某抓住莫某乙，李2某、董某各持1把菜刀将莫某乙的右背部、右臀部、右上臂等处砍伤。当晚，被告人何某付给谢某人民币9000元。莫某乙的伤情经医院诊断为：1、失血性休克；2、右上臂刀伤－（1）右桡神经断裂；（2）右肱骨开放性劈裂骨折；3、右背部刀伤并肋骨开放性骨折；4、全身多处刀伤并肌肉断裂。经法医鉴定，莫某乙右腕垂腕、不能背伸，属于重伤；其右上肢、背部及右臀部多处软组织创伤的创口单条超过10CM、累计长度超过15CM，属于轻伤；其人身伤害致右手损伤致右腕关节丧失功能属于八级××；右手丧失功能程度属于九级××。为支持上述指控的犯罪事实，桂林市叠彩区人民检察院当庭宣读和出示了书证、证人证言、被害人报案材料及陈述、被告人供述及辩解、鉴定结论等证据。根据上述证据，桂林市叠彩区人民检察院认为被告人李3某的行为已构成××罪，提请法院依照《中华人民共和国刑法》××××的规定对被告人李3某予以惩处。"
    # result = modelHelper.predictMultiLabel(predict_fact)
    # print(result)