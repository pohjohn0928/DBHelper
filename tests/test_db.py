from utils.db_helper import DBHelper
from utils.data_helper import DataHelper
from config import DBSetting
from datetime import datetime


if __name__ == '__main__':
    db_setting = DBSetting()
    data_helper = DataHelper()
    data = data_helper.getCleanCSVData()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        print("db method")
        # db_helper.TruncateTable("report")
        # db_helper.TruncateTable("task")
        # db_helper.InserCSVData(data, len(data))
        # db_helper.InitTaskTable()
        #
        # row_data = db_helper.getCovidData()
        # key_word = '武漢肺炎'
        # data_helper.dataToCSV(row_data,key_word)

        # db_helper.CreatTaskTable("task")
        # db_helper.InitTaskTable()
        # print(db_helper.InsertToTaskTable("task5","This is task 5"))
        # print(db_helper.UpdateTaskTable(1,"task1","This is task 1"))
        # print(db_helper.DeleteTaskData(1))
        # db_helper.TruncateTable("task")
        # print(db_helper.GetTaskTableInfo())

        # db_helper.CreatTaskTable("task")
        # db_helper.InserCSVData(data,len(data))
        # print(db_helper.InsertData("123",1))
        # print(db_helper.InsertData("456",1001,1))
        # db_helper.UpdateData("666",2,1)
        # db_helper.DeleteData(2)
        # print(db_helper.SelectData(1000))
        # print(db_helper.SelectDataById("report", 99))
        # db_helper.TruncateTable("report")

        # db_helper.DropTable("task")
        # db_helper.CreatTable("report")

        # db_helper.CreateDocTable("documents")
        # db_helper.TruncateTable("documents")
        # db_helper.InsertCSVDataToDoc(data,len(data))