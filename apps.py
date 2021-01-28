from flask import Flask,request,render_template
from utils.db_helper import DBHelper

app = Flask(__name__)
                                    # user = request.args.get('nm')
@app.route('/')
def home_page():
    return "This is Home Page"

@app.route('/html')
def html():
    return render_template("index.html",title = "test")

@app.route('/login',methods = ['POST'])
def wellcome():
    name = request.values['name']
    print(f"{name} is logging ! ")
    return render_template('login.html',name = name)

@app.route('/news')
def news():
    db_helper = DBHelper()
    return db_helper.GetCSVData(1000)

if __name__ == '__main__':
    app.run(debug=True)





