import pymysql
from config import DBSetting

class DBHelper:
    def __init__(self,host,user,password,db,port):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, port=port)
        self.cursor = self.conn.cursor()

    def InserCSVData(self, data, num_of_data: int):
        for i in range(num_of_data):
            sql = f"INSERT INTO report VALUES('{data[i]}','','','{i + 1}')"
            self.cursor.execute(sql)
        self.conn.commit()

    def InsertData(self, str, id: int):
        sql = f"INSERT INTO report VALUES('{str}','','','{id}')"
        try:
            self.cursor.execute(sql)
        except:
            print("id already exist")
        self.conn.commit()

    def UpdateData(self,str,id):
        sql = f"UPDATE report set content = '{str}' where id = '{id}'"
        self.cursor.execute(sql)
        self.conn.commit()

    def DeleteData(self,id):
        sql = f"delete from report where id = {id}"
        self.cursor.execute(sql)
        self.conn.commit()

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

    def TruncateTable(self):
        sql = "TRUNCATE TABLE report"
        self.cursor.execute(sql)
        self.conn.commit()

    def CreatTable(self,tableName):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        for table in tables:
            print(table[0])
        sql = f"CREATE TABLE {tableName}(id int,content varchar(100),label varchar(10));"
        self.cursor.execute(sql)
        self.conn.commit()

    def DropTable(self,tableName):
        sql = f"DROP TABLE {tableName};"
        self.cursor.execute(sql)
        self.conn.commit()

    def ConnClose(self):
        self.conn.close()