from utils.db_helper import DBHelper
from utils.data_helper import DataHelper
from config import DBSetting

if __name__ == '__main__':
    db_setting = DBSetting()
    data_helper = DataHelper()
    data = data_helper.getCleanCSVData()
    with DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db) as db_helper:
        print("db method")
        # db_helper.InserCSVData(data,200)
        db_helper.InsertData("123",1,1)
        # print(db_helper.InsertData("456",1001,1))
        # db_helper.UpdateData("666",2,1)
        # db_helper.DeleteData(2)
        # print(db_helper.SelectData(1000))
        # print(db_helper.SelectDataById("report", 99))
        # db_helper.TruncateTable("report")

        # db_helper.DropTable("report")
        # db_helper.CreatTable("report")

        # db_helper.CreateDocTable("documents")
        # db_helper.TruncateTable("documents")
        # db_helper.InsertCSVDataToDoc(data,len(data))