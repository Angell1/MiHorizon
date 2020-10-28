# -*- coding: <encoding name> -*-
from flask import Flask,request, jsonify,render_template
import importlib
import unittest
import inspect
import time
from sqlalchemy import create_engine
from marshmallow import ValidationError
from config import setting
import configparser as cparser
from httpserver.src import model
from lib.newReport import new_report
from package.HTMLTestRunner import HTMLTestRunner


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

# http://127.0.0.1:8081/api//testcase/case/?filename=test1API&classename=UCTestCase&funcname=testCreateFolder
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/api//testcase/case/')
def excetestcase():
    requests = handler((dict(request.args)))  # 获取所有接收到的参数。
    error = None
    data = None
    # 反序列化
    try:
        schema = model.TestcaseinputSchema()
        data =  schema.load(requests)
        data= schema.dump(data)
        # print(data)
    except ValidationError as err:
        error = err.messages
        # print(error)
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    if error != None:
        returnres['msg'] = error
        return jsonify(returnres)
    else:
        moud, clas = dynamicimport(data['filename'], data['classname'])
        # 构造测试集
        suite = unittest.TestSuite()
        suite.addTest(clas(data['funcname']))
        # 执行测试，生成测试报告
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        filename = setting.TEST_REPORTDIR + '/' + now + 'result.html'
        fp = open(filename, 'wb')
        runner = HTMLTestRunner(stream=fp, title='发布会系统接口自动化测试报告',
                                description='环境：windows 10 浏览器：chrome',
                                tester='-零')
        runner.run(suite)
        fp.close()
        report = new_report(setting.TEST_REPORTDIR)  # 调用模块生成最新的报告
        return jsonify(returnres)

def handler(requests):
    for i in requests:
        print(i)
        if requests[i][0]:
            requests[i] = requests[i][0]
        else:
            requests[i] = ""
    print(requests)
    return   requests



# http://127.0.0.1:8080/api/module/?file=test1API&class=UCTestCase
# http://127.0.0.1:8080/api/module/?file=test1API&class=UCTestCase,UTest1
@app.route('/api/testmodule/module/')
def excetestmodule():
    requests = request.args  # 获取所有接收到的参数。
    print(requests.get('file'))
    filename = requests.get('file')
    print(requests.get('class'))
    clasname = requests.get('class')
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    if len(clasname.split(',')) == 1:
        moud, clas = dynamicimport(filename, clasname)
        # # 构造测试集
        suite = unittest.TestSuite()
        for name, function in inspect.getmembers(clas, inspect.isfunction):
            if 'test' in name:
                suite.addTest(clas(name))
        runner = unittest.TextTestRunner()
        runner.run(suite)
    else:
        suite = unittest.TestSuite()
        moud = importlib.import_module('testcase.%s' % filename, package='testcase')
        for name, class_ in inspect.getmembers(moud, inspect.isclass):
            if name in clasname.split(','):
                for name, method in inspect.getmembers(class_, inspect.isfunction):
                    if 'test' in name:
                        print(name)
                        suite.addTest(class_(name))
        # 执行测试
        runner = unittest.TextTestRunner()
        runner.run(suite)
    return jsonify(returnres)


#获取测试示例
# http://127.0.0.1:8081/api/testcase/
@app.route('/api/testcase/')
def testcase():
    requests = request.args  # 获取所有接收到的参数。
    print(request.args)
    # 反序列化 pass
    # 获取数据
    Conn = ConnConfig()
    with Conn.engine.connect() as db:
            sql = "select * from " + 'testtable where test_tablename_type = 0 ;'
            result = db.execute(sql)
    result = result.fetchall()
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    for i in result:
        with Conn.engine.connect() as db:
                sql = "select * from " + '%s;' % str(i[1])
                result = db.execute(sql)
        result = result.fetchall()
        reslist = []
    # 序列化
        for res in result:
            # print(res)
            testcase = model.TestCase(id=res[0], test_pro=res[1],test_id=res[2],test_target=res[3],test_level=res[4],test_condition = res[5],test_input=res[6],test_step=res[7],test_output=res[8],is_connect=res[9],test_module = res[10])
            schema = model.TestCaseSchema()
            dumpres = schema.dump(testcase)
            reslist.append(dumpres)
     # 对序列化结果进行过滤、排序 pass
        returnres['result'] = reslist
    # print(returnres)
    return jsonify(returnres)

#获取测试用例执行结果
# http://127.0.0.1:8081/api/testresult/
@app.route('/api/testresult/')
def testresult():
    requests = request.args  # 获取所有接收到的参数。
    # 反序列化 pass
    # 获取数据
    Conn = ConnConfig()
    with Conn.engine.connect() as db:
            sql = "select * from " + 'testtable where test_tablename_type = 1 ;'
            result = db.execute(sql)
    result = result.fetchall()
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    for i in result:
        with Conn.engine.connect() as db:
                sql = "select * from " + '%s;' % str(i[1])
                result = db.execute(sql)
        result = result.fetchall()
        reslist = []
    # 序列化
        for res in result:
            print(res)
            testcase = model.TestCaseres(id=res[0], test_caseid=res[1],test_time=res[2],test_pro=res[3],test_target=res[5],test_level=res[6],test_condition = res[7],test_input=res[6],test_step=res[8],test_output=res[9],test_module = res[10])
            schema = model.TestCaseresSchema()
            dumpres = schema.dump(testcase)
            reslist.append(dumpres)
     # 对序列化结果进行过滤、排序 pass
        returnres['result'] = reslist
    # print(returnres)
    return jsonify(returnres)

#获取测试用例执行结果
# http://127.0.0.1:8081/api/testresult/
@app.route('/api/report/')
def testreport():
    requests = request.args  # 获取所有接收到的参数。
    print(requests.get('reportname'))
    reportname = requests.get('reportname')

    return render_template('%s' %reportname)

def dynamicimport(filename,clasname):
    # 动态导入包
    moud = importlib.import_module('testcase.%s' % filename, package='testcase')
    # 实例化类
    clas = getattr(moud, clasname)

    return moud,clas



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8081,debug=True)