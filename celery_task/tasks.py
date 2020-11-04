from __future__ import absolute_import, unicode_literals
from .celery import app
from config import setting
import configparser as cparser
from sqlalchemy import create_engine
import unittest
import inspect
import time
import importlib
from package.HTMLTestRunner import HTMLTestRunner
from lib.newReport import new_report

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
        self.DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(self.USERNAME, self.PASSWORD, self.HOST, self.PORT,
                                                              self.DATABASE)
        # 创建引擎
        self.engine = create_engine(self.DB_URI)

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task
def create_timingtask(data):
    print("celery接收参数:",data)
    Conn = ConnConfig()
    with Conn.engine.connect() as db:
        sql = "select moudle_name,test_filename,test_classname from " + 'moudletable where id = %d;' % (data['moudleid'])
        # print(sql)
        result = db.execute(sql)
        result = result.fetchall()
        if len(result[0][1].split(',')) == 1:
            moud, clas = dynamicimport(result[0][1], result[0][2])
            # 构造测试集
            suite = unittest.TestSuite()
            for name, function in inspect.getmembers(clas, inspect.isfunction):
                if 'test' in name:
                    suite.addTest(clas(name))
        else:
            suite = unittest.TestSuite()
            moud = importlib.import_module('testcase.%s' % result[0][1], package='testcase')
            for name, class_ in inspect.getmembers(moud, inspect.isclass):
                if name in result[0][2].split(','):
                    for name, method in inspect.getmembers(class_, inspect.isfunction):
                        if 'test' in name:
                            print(name)
                            suite.addTest(class_(name))
        # 执行测试，生成测试报告
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        filename = setting.TEST_REPORTDIR + '/' + now + '_%s_result.html' % (data['moudleid'])
        fp = open(filename, 'wb')
        runner = HTMLTestRunner(stream=fp, title='测试报告',
                                    description='环境：windows 10 浏览器：chrome',
                                    tester='-')
        runner.run(suite)
        fp.close()
        new_report(setting.TEST_REPORTDIR)  # 调用模块生成最新的报告


@app.task
def create_steptask(data):
    print("celery接收参数:", data)
    Conn = ConnConfig()
    with Conn.engine.connect() as db:
        sql = "select moudle_name,test_filename,test_classname from " + 'moudletable where id = %d;' % (
        data['moudleid'])
        # print(sql)
        result = db.execute(sql)
        result = result.fetchall()
        if len(result[0][1].split(',')) == 1:
            moud, clas = dynamicimport(result[0][1], result[0][2])
            # 构造测试集
            suite = unittest.TestSuite()
            for name, function in inspect.getmembers(clas, inspect.isfunction):
                if 'test' in name:
                    suite.addTest(clas(name))
        else:
            suite = unittest.TestSuite()
            moud = importlib.import_module('testcase.%s' % result[0][1], package='testcase')
            for name, class_ in inspect.getmembers(moud, inspect.isclass):
                if name in result[0][2].split(','):
                    for name, method in inspect.getmembers(class_, inspect.isfunction):
                        if 'test' in name:
                            print(name)
                            suite.addTest(class_(name))
        # 执行测试，生成测试报告
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        filename = setting.TEST_REPORTDIR + '/' + now + '_%s_result.html' % (data['moudleid'])
        fp = open(filename, 'wb')
        runner = HTMLTestRunner(stream=fp, title='测试报告',
                                description='环境：windows 10 浏览器：chrome',
                                tester='-')
        runner.run(suite)
        fp.close()
        new_report(setting.TEST_REPORTDIR)  # 调用模块生成最新的报告
        task_id = create_steptask.apply_async(([data]), countdown=int(data['date3']) * 60)
        # with Conn.engine.connect() as db:
        #     sql = "update  tasktable  set task_id = '%s' where moudle_id = '%s' and task_context =  '%s';" % (
        #         task_id,data['moudleid'],data['date1'] +' ' + data['date2'])
        #     # print(sql)
        #     result = db.execute(sql)



def dynamicimport(filename, clasname):
    # 动态导入包
    moud = importlib.import_module('testcase.%s' % filename, package='testcase')
    # 实例化类
    clas = getattr(moud, clasname)

    return moud, clas