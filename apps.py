from flask import Flask,request,render_template
from utils.db_helper import DBHelper
from config import DBSetting

app = Flask(__name__)
                                    # user = request.args.get('nm')
                                    # name = request.values['name']
@app.route('/')
def home_page():
    return render_template("index.html",title = "DB")

@app.route('/insert',methods = ["POST"])
def insert():
    id = request.values['id']
    content = request.values['content']
    taskId = request.values['taskId']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.InsertData(content,id,taskId)
        return result


@app.route('/update',methods = ["POST"])
def update():
    id = request.values['id']
    content = request.values['content']
    task_id = request.values['task_id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.UpdateData(content,id,task_id)
        return result

@app.route('/delete',methods = ["POST"])
def idDelete():
    id = request.values['id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        result = db_helper.DeleteData(id)
        return result

@app.route('/searchByTask',methods = ["POST"])
def task():
    taskNum = request.values['task']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        news = db_helper.SelectDataByTask('report',int(taskNum))
        result = {
            "id" : [],
            "content" : [],
            "task_id" : []
        }
        for new in news:
            result["id"].append(new[3])
            result["content"].append(new[0])
            result["task_id"].append(new[4])
    return result

@app.route('/searchById',methods = ["POST"])
def id():
    id = request.values['id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        news = db_helper.SelectDataById('report', id)
    if news == ():
        return "false"
    else:
        result = {
            "id" : news[0][3],
            "content" : news[0][0],
            "task_id" : news[0][4]
        }
        return result


if __name__ == '__main__':
    app.run(debug=True)





