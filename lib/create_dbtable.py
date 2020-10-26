import os
from sqlalchemy import create_engine
from config import setting
import configparser as cparser

# --------- 读取config.ini配置文件 ---------------
cf = cparser.ConfigParser()
cf.read(setting.TEST_CONFIG,encoding='UTF-8')
HOST = cf.get("mysqlconf","host")
PORT = cf.get("mysqlconf","port")
USERNAME = cf.get("mysqlconf","user")
PASSWORD = cf.get("mysqlconf","password")
DATABASE = cf.get("mysqlconf","db_name")
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)
#创建引擎
engine = create_engine(DB_URI)
#获取文件的上级目录，对应下图的路径
# 此处获取目录中所有的文件名称
file_name=os.listdir(setting.SOURCE_DIR)



with engine.connect() as db:

        sql = "create table "
        db.execute(sql)
