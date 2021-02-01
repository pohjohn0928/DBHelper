from flask import Flask,request,render_template
from utils.db_helper import DBHelper
from config import DBSetting

app = Flask(__name__)
                                    # user = request.args.get('nm')
                                    # name = request.values['name']
@app.route('/')
def home_page():
    return render_template("index.html",title = "tasks")

@app.route('/insert',methods = ["POST"])
def insert():
    id = request.values['id']
    content = request.values['content']
    taskId = request.values['taskId']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        return f'<script>alert("{db_helper.InsertData(content,id,taskId)}")</script>'

@app.route('/update',methods = ["POST"])
def update():
    id = request.values['id']
    content = request.values['content']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        return f'<script>alert("{db_helper.UpdateData(content,id)}")</script>'

@app.route('/delete',methods = ["POST"])
def idDelete():
    id = request.values['id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        return f'<script>alert("{db_helper.DeleteData(id)}")</script>'

@app.route('/searchByTask',methods = ["POST"])
def task():
    taskNum = request.values['task']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        news = db_helper.SelectDataByTask('report',int(taskNum))
    return render_template("task.html",news = news,db_helper = db_helper)

@app.route('/searchById',methods = ["POST"])
def id():
    id = request.values['id']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        news = db_helper.SelectDataById('report', id)
    return render_template("id.html",news = news)

if __name__ == '__main__':
    app.run(debug=True)





