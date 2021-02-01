import pymysql
import logging


class DBHelper:
    def __init__(self, host, user, password, db):
        self.conn = pymysql.connect(host=host, user=user, password=password)
        self.cursor = self.conn.cursor()
        self.db = db
        FORMAT = '%(asctime)s %(levelname)s: %(message)s'
        DATE_FORMAT = '%Y%m%d %H:%M:%S'
        logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATE_FORMAT, filename='db.log', filemode='w')

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

    def InsertData(self, str, id: int, taskId: int):
        checkSql = f"select * from report where id={id}"
        self.cursor.execute(checkSql)
        if self.cursor.fetchall() == ():
            sql = f"INSERT INTO report VALUES('{str}','','','{id}','{taskId}')"
            self.cursor.execute(sql)
            return f"{str} is inserted to report with id : {id} and task id : {taskId}"
        else:
            return "Id already exist!"

    def UpdateData(self, str, id: int):
        checkSql = f"select * from report where id={id}"
        self.cursor.execute(checkSql)
        if self.cursor.fetchall() != ():
            sql = f"UPDATE report set content = '{str}' where id = '{id}'"
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        logging.debug("Database closed..")
