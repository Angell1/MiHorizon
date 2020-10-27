import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from config import setting
import configparser as cparser


class ConnConfig():
    def __init__(self):
        # --------- 读取config.ini配置文件 ---------------
        cf = cparser.ConfigParser()
        cf.read(setting.TEST_CONFIG, encoding='UTF-8')
        self.HOST = cf.get("mysqlconf", "host")
        self.PORT = cf.get("mysqlconf", "port")
        self.USERNAME = cf.get("mysqlconf", "user")
        self.PASSWORD = cf.get("mysqlconf", "password")
        self.DATABASE = cf.get("mysqlconf", "db_name")
        self.DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(self.USERNAME, self.PASSWORD, self.HOST, self.PORT,self.DATABASE)
        # 创建引擎
        self.engine = create_engine(self.DB_URI)

    #更新完整的excel测试用例到数据库
    def pdtomysql(self):
        # 获取文件的上级目录，对应下图的路径
        # 此处获取目录中所有的文件名称
        file_name = os.listdir(setting.SOURCE_DIR)
        tablenamelist = []
        with self.engine.connect() as db:
            for i in range(len(file_name)):
                tablename = file_name[i][0:-5]
                tablenamelist.append(tablename)
                excel = pd.read_excel(os.path.join(setting.SOURCE_DIR, file_name[i]))
                sql = "create table " + file_name[i][0:-5] + "(id int primary key auto_increment," \
                                                             "test_pro char(30) not null," \
                                                             "test_id char(20)," \
                                                             "test_target char(100)," \
                                                             "test_level char(20)," \
                                                             "test_condition char(100)," \
                                                             "test_input char(100)," \
                                                             "test_step char(100)," \
                                                             "test_output char(100)," \
                                                             "is_connect INT," \
                                                             "test_module char(30));"
                db.execute(sql)
                for i in range(len(excel.index.values)):

                    sql = "insert into " + tablename + "(test_pro,test_id,test_target,test_level,test_condition,test_input,test_step,test_output,is_connect,test_module)" + " values('%s','%s','%s','%s','%s','%s','%s','%s',0,'%s')" % (
                        excel.iloc[i].测试项目, excel.iloc[i].用例编号, excel.iloc[i].测试目的, excel.iloc[i].重要级别,
                        excel.iloc[i].预置条件, excel.iloc[i].测试输入, excel.iloc[i].操作步骤, excel.iloc[i].预期输出,excel.iloc[i].测试模块)
                    db.execute(sql)
                sql = "create table " + tablename + '_result' + "(id int primary key auto_increment," \
                                                                "test_caseid INT," \
                                                                "test_time date," \
                                                                "test_pro char(30) not null," \
                                                                "test_id INT," \
                                                                "test_target char(100)," \
                                                                "test_level char(20)," \
                                                                "test_condition char(100)," \
                                                                "test_input char(100)," \
                                                                "test_step char(100)," \
                                                                "test_output char(100)," \
                                                                "test_mould char(30));"
                db.execute(sql)
        return tablenamelist

    def createtesttable(self,tablenamelist):
        with self.engine.connect() as db:
            sql = "create table " + 'testtable' + "(id int primary key auto_increment," \
                                                      "test_tablename char(30) not null," \
                                                      "test_tablename_type char(10));"
            db.execute(sql)
            for table in tablenamelist:
                sql = "insert into " + 'testtable' + "(test_tablename,test_tablename_type)" + " values('%s','%s')" % (table,'0')
                db.execute(sql)
                sql = "insert into " + 'testtable' + "(test_tablename,test_tablename_type)" + " values('%s','%s')" % (table+'_result', '1')
                db.execute(sql)


    def createcasetable(self):
        with self.engine.connect() as db:
            sql = "create table " + 'tecasetable' + "(id int primary key auto_increment," \
                                                    "test_id INT," \
                                                    "test_filename char(30)," \
                                                    "test_classname char(30)," \
                                                    "test_funcname char(30)," \
                                                    "test_module char(30));"
            db.execute(sql)

# Conn = ConnConfig()
# tablenamelist = Conn.pdtomysql()
# Conn.createtesttable(tablenamelist)



Conn = ConnConfig()
Conn.createcasetable()