import pymysql
import logging
from datetime import datetime

class DBHelper:
    def __init__(self, host, user, password, db):
        self.conn = pymysql.connect(host=host, user=user, password=password)
        self.cursor = self.conn.cursor()
        self.db = db
        FORMAT = '%(asctime)s %(levelname)s: %(message)s'
        DATE_FORMAT = '%Y%m%d %H:%M:%S'
        logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATE_FORMAT, filename='C:\\Users\\taisiangbo\\Desktop\\python\\dbHelper\\log\\db.log', filemode='a')

    def __enter__(self):
        sql = "show databases"
        self.cursor.execute(sql)
        databases = self.cursor.fetchall()
        databases_exist = 0
        for database in databases:
            if database[0] == self.db:
                databases_exist = 1
        if databases_exist == 0:
            logging.error(f"{self.db} does not exist!")

        else:
            logging.debug(f"Using database {self.db}")
            sql = f"use {self.db}"
            self.cursor.execute(sql)
            return self

    def InserCSVData(self, data, num_of_data: int):
        for i in range(num_of_data):
            sql = f"INSERT INTO report VALUES('{data[i]}','','','{i + 1}','{int(i / 200) + 1}')"
            self.cursor.execute(sql)

    def InsertData(self, str, taskId: int):
        sql = f"INSERT INTO report (content,label,other,taskId) VALUES('{str}','','','{taskId}')"
        self.cursor.execute(sql)
        return f"{str} is inserted to report with task id : {taskId}"

    def UpdateData(self, str, id: int,taskId:int):
        checkSql = f"select * from report where id={id}"
        self.cursor.execute(checkSql)
        if self.cursor.fetchall() != ():
            sql = f"UPDATE report set content = '{str}', taskId = '{taskId}' where id = '{id}'"
            self.cursor.execute(sql)
            return f"id : {id} is updated with content : {str}"
        else:
            return f"Id : {id} dose not exist yet"

    def DeleteData(self, id: int):
        checkSql = f"select * from report where id={id}"
        self.cursor.execute(checkSql)
        if self.cursor.fetchall() != ():
            sql = f"delete from report where id = {id}"
            self.cursor.execute(sql)
            return f"id : {id} is deleted"
        else:
            return f"{id} dose not exist yet"

    def SelectData(self, num_of_data: int):
        sql = f"select * from report limit {num_of_data}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data_text = ""
        counter = 0
        for txt in data:
            data_text += f"{counter + 1} : " + txt[0] + "</br>"
            counter += 1
        return data_text

    def LabelReportTable(self,id,label):
        sql = f"UPDATE report set label = '{label}' where id = '{id}'"
        self.cursor.execute(sql)
        return f"Update id {id} with tag {label}"

    def SelectDataById(self, tableName, id):
        sql = f"select * from {tableName} where id={id}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def SelectDataByTask(self, tableName, taskNum: int):
        sql = f"select * from {tableName} where taskId={taskNum}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def TruncateTable(self, tableName):
        sql = f"TRUNCATE TABLE {tableName}"
        self.cursor.execute(sql)

    def CreatTable(self, tableName):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        table_exist = 0
        for table in tables:
            if table[0] == tableName:
                table_exist = 1
        if table_exist == 0:
            sql = f"CREATE TABLE {tableName}(content varchar(10000),label varchar(100),other varchar(100),id int,taskId int,PRIMARY KEY (id));"
            self.cursor.execute(sql)

        else:
            logging.error(f"Table Name '{tableName}' already exist")

    def DropTable(self, tableName):
        sql = f"DROP TABLE {tableName};"
        try:
            self.cursor.execute(sql)
        except Exception:
            logging.error(f"Can't find out the table {tableName}")


    def CreateDocTable(self, tableName):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        table_exist = 0
        for table in tables:
            if table[0] == tableName:
                table_exist = 1
        if table_exist == 0:
            sql = f"CREATE TABLE {tableName}(doc_id int,content varchar(10000),task_id int,label varchar(100),PRIMARY KEY (doc_id));"
            self.cursor.execute(sql)
        else:
            logging.error(f"Table Name '{tableName}' already exist")

    def InsertCSVDataToDoc(self,data,num_of_data: int):
        for i in range(num_of_data):
            sql = f"INSERT INTO documents VALUES('{i + 1}','{data[i]}','{int(i / 200) + 1}','')"
            self.cursor.execute(sql)



    #Task table
    def CreatTaskTable(self,tableName):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        table_exist = 0
        for table in tables:
            if table[0] == tableName:
                table_exist = 1
        if table_exist == 0:
            sql = f"CREATE TABLE {tableName}(id int AUTO_INCREMENT,name varchar(100),tags varchar(100),description varchar(20000),create_time varchar(100),Update_time varchar(100),PRIMARY KEY (id));"
            self.cursor.execute(sql)
        else:
            logging.error(f"Table Name '{tableName}' already exist")

    def InitTaskTable(self):
        sql = "SELECT * FROM report GROUP BY taskId HAVING count(*)>1"
        self.cursor.execute(sql)
        for data in self.cursor.fetchall():
            self.InsertToTaskTable(f"task{data[4]}","",f"This is task{data[4]}")
        return "Finish Initialize"

    def GetTaskTableInfo(self):
        sql = f"select * from task where 1"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def InsertToTaskTable(self,name,tags,description):
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        sql = f"INSERT INTO task (name,tags,description,create_time,Update_time) VALUES('{name}','{tags}','{description}','{current_time}','{current_time}')"
        self.cursor.execute(sql)
        return "Finish Insert"

    def UpdateTaskTable(self,id:int,name,tags,description):
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        sql = f"UPDATE task set name = '{name}',tags = '{tags}', description = '{description}', Update_time ='{current_time}' where id = '{id}'"
        self.cursor.execute(sql)
        return f"id : {id} is updated name : '{name}' , tags = {tags} and description : '{description}'"

    def DeleteTaskData(self,id: int):
        checkSql = f"select * from task where id={id}"
        self.cursor.execute(checkSql)
        if self.cursor.fetchall() != ():
            sql = f"delete from task where id = {id}"
            self.cursor.execute(sql)
            return f"id : {id} is deleted"
        else:
            return f"{id} dose not exist yet"

    def ShowLabelNumber(self,taskId):
        sql = f"SELECT * FROM report where taskId={taskId}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        labelDic = {}

        for new in data:
            if new[1] in labelDic.keys():
                labelDic[f"{new[1]}"] += 1
            else:
                labelDic[f"{new[1]}"] = 1

        return labelDic


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        logging.debug("Database closed..")
