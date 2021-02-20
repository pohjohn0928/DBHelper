from flask import Flask, request, render_template
from utils.db_helper import DBHelper
from utils.model_helper import ModelHelper
from config import DBSetting
import os
from utils.data_helper import DataHelper
app = Flask(__name__)


# user = request.args.get('nm')
# name = request.values['name']
@app.route('/')
def taskTable():
    return render_template("task.html")


@app.route('/showTaskTable', methods=['POST'])
def showTaskTable():
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        taskInfo = db_helper.GetTaskTableInfo()
        result = {
            "id": [],
            "name": [],
            "tags": [],
            "description": [],
            "create_time": [],
            "Update_time": []
        }
        for info in taskInfo:
            result["id"].append(info[0])
            result["name"].append(info[1])
            result["tags"].append(info[2])
            result["description"].append(info[3])
            result["create_time"].append(info[4])
            result["Update_time"].append(info[5])
    return result


@app.route('/tables', methods=["POST", "GET"])
def tables():
    return render_template("index.html", title="DB")


@app.route('/getTaskNum', methods=["POST"])
def getTaskNum():
    taskNum = request.args.get('taskId')
    print(taskNum)
    return taskNum


@app.route('/insert', methods=["POST"])
def insert():
    content = request.values['content']
    label = request.values['label']
    taskId = request.values['taskId']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.InsertData(content,label, taskId)
        return result

@app.route('/ReadCSVFileToDB', methods=["POST"])
def ReadCSVFileToDB():
    content = request.values["content"]
    label = request.values["label"]
    taskId = request.values['taskId']
    db_setting = DBSetting()
    content = content.replace("[","").replace("]","").replace("\"","")
    content = content.split(",")
    label = label.replace("\\","").replace("[","").replace("]","").replace("\"","").replace("r","")
    label = label.split(",")
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        for i in range(len(content)):
            db_helper.ReadCSVFileToDB(content[i],label[i],taskId)
        return "Finish Insert CSV"



@app.route('/update', methods=["POST"])
def update():
    id = request.values['id']
    content = request.values['content']
    task_id = request.values['task_id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.UpdateData(content, id, task_id)
        return result


@app.route('/delete', methods=["POST"])
def idDelete():
    id = request.values['id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.DeleteData(id)
        return result


@app.route('/searchByTask', methods=["POST", "GET"])
def task():
    taskNum = request.values['task']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        news = db_helper.SelectDataByTask('report', int(taskNum))
        result = {
            "id": [],
            "content": [],
            "task_id": [],
            "label": []
        }
        for new in news:
            result["id"].append(new[3])
            result["content"].append(new[0])
            result["task_id"].append(new[4])
            result["label"].append(new[1])
    return result


@app.route('/searchById', methods=["POST"])
def id():
    id = request.values['id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        news = db_helper.SelectDataById('report', id)
    if news == ():
        return "false"
    else:
        print(news)
        result = {
            "id": news[0][3],
            "content": news[0][0],
            "label" : news[0][1],
            "task_id": news[0][4]
        }
        return result


@app.route('/upateTaskTable', methods=["POST"])
def upateTaskTable():
    id = request.values['id']
    name = request.values['name']
    tags = request.values['tags']
    description = request.values['description']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.UpdateTaskTable(id, name, tags, description)
        return result


@app.route('/deleteTaskData', methods=["POST"])
def deleteTaskData():
    id = request.values['id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.DeleteTaskData(id)
        return result


@app.route('/insertTaskData', methods=["POST"])
def insertTaskData():
    name = request.values['name']
    tags = request.values['tag']
    description = request.values['description']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.InsertToTaskTable(name, tags, description)
        return result


@app.route('/labelReportTable', methods=["POST"])
def labelReportTable():
    id = request.values['id']
    tags = request.values['tags']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.LabelReportTable(id, tags)
        return result


@app.route('/showLabelNum', methods=["POST"])
def showLabelNum():
    taskNum = request.values['task']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.ShowLabelNumber(taskNum)
    return result

@app.route('/autoLabelSVM', methods=["POST"])
def autoLabel():
    taskNum = request.values['taskId']
    db_setting = DBSetting()
    model_helper = ModelHelper()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        datas = db_helper.SelectDataByTask("report",taskNum)
        for data in datas:
            db_helper.LabelReportTable(data[3],model_helper.predictBySVM(data[0])[0])
        return "finish"

@app.route('/autoLabelXgboost', methods=["POST"])
def autoLabelXgboost():
    taskNum = request.values['taskId']
    db_setting = DBSetting()
    model_helper = ModelHelper()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        datas = db_helper.SelectDataByTask("report",taskNum)
        for data in datas:
            db_helper.LabelReportTable(data[3],model_helper.predictByXgboost(data[0])[0])
        return "finish"

@app.route('/keywordSelect', methods=["POST"])
def keywordSelect():
    keyword = request.values['keyword']
    db_setting = DBSetting()
    data_helper = DataHelper()

    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        row_data = db_helper.getKeyWordData()
        data_helper.dataToCSV(row_data, keyword)
        dirname = os.path.dirname(__file__)
        return f"The path of the CSV file is {dirname}"

if __name__ == '__main__':
    app.run(debug=True)
