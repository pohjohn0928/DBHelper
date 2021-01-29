from flask import Flask,request,render_template
from utils.db_helper import DBHelper
from config import DBSetting
import pandas as pd

app = Flask(__name__)
                                    # user = request.args.get('nm')
                                    # name = request.values['name']
@app.route('/')
def home_page():
    return render_template("index.html",title = "tasks")

@app.route('/task',methods = ["POST"])
def task():
    taskNum = request.values['task']
    db_setting = DBSetting()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db, db_setting.port) as db_helper:
        news = db_helper.SelectDataByTask('report',int(taskNum))
    return render_template("task.html",news = news,db_helper = db_helper)

if __name__ == '__main__':
    app.run(debug=True)





