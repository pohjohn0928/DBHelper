from utils.db_helper import DBHelper
from utils.data_helper import DataHelper
from config import DBSetting

if __name__ == '__main__':
    db_setting = DBSetting()
    data_helper = DataHelper()
    db_helper = DBHelper(db_setting.host, db_setting.user, db_setting.password, db_setting.db, db_setting.port)
    data = data_helper.getCleanCSVData()

    # db_helper.InserCSVData(data,1000)
    # db_helper.InsertData("123",1001)
    # db_helper.InsertData("456",1002)
    # db_helper.UpdateData("666",2)
    # db_helper.DeleteData(2)
    # print(db_helper.SelectData(1000))
    # db_helper.TruncateTable()

    db_helper.CreatTable("poh")
    # db_helper.DropTable("report")
    db_helper.ConnClose()
