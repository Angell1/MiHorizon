# -*- coding: <encoding name> -*-
from flask import Flask, request, jsonify, render_template
import importlib
import unittest
import inspect
import time
import random
import os
from sqlalchemy import create_engine
from marshmallow import ValidationError
from config import setting
import configparser as cparser
from httpserver.src import model
from lib.newReport import new_report
from package.HTMLTestRunner import HTMLTestRunner
from celery_task import tasks

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


# 后端请求接口：执行测试用例
# http://127.0.0.1:8081/api/testcaseS/case/?filename=test1API&classname=UCTestCase&funcname=testCreateFolder&testid=ST-121
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/api/testcaseS/case/')
def excetestcase():
    requests = handler((dict(request.args)))  # 获取所有接收到的参数。
    error = None
    data = None
    # 反序列化
    try:
        schema = model.TestcaseinputSchema()
        data = schema.load(requests)
        data = schema.dump(data)
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
        filename = setting.TEST_REPORTDIR + '/' + now + '_%s_result.html' % (data['testid'])
        fp = open(filename, 'wb')
        runner = HTMLTestRunner(stream=fp, title='发布会系统接口自动化测试报告',
                                description='环境：windows 10 浏览器：chrome',
                                tester='-零')
        runner.run(suite)
        fp.close()
        report = new_report(setting.TEST_REPORTDIR)  # 调用模块生成最新的报告
        return jsonify(returnres)


# 前端请求接口：执行测试用例
# http://127.0.0.1:8081/api/testcase/case/?testid=ST-12
@app.route('/api/testcase/case/')
def newexcetestcase():
    # ID
    requests = handler((dict(request.args)))  # 获取所有接收到的参数。
    error = None
    data = None
    # 反序列化
    try:
        schema = model.TestreportlistSchema()
        data = schema.load(requests)
        data = schema.dump(data)
        # print(data)
    except ValidationError as err:
        error = err.messages
        # print(error)
        # 获取数据
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    reslist = []
    if error != None:
        returnres['msg'] = error
        return jsonify(returnres)
    else:
        if 'testid' in data:
            Conn = ConnConfig()
            with Conn.engine.connect() as db:
                sql = "select test_filename,test_classname,test_funcname from " + 'casetable where test_id = "%s";' % (
                data['testid'])
                print(sql)
                result = db.execute(sql)
            result = result.fetchall()
            if len(result):
                print("执行测试用例的脚本绑定！")
                moud, clas = dynamicimport(result[0][0], result[0][1])
                # 构造测试集
                suite = unittest.TestSuite()
                suite.addTest(clas(result[0][2]))
                # 执行测试，生成测试报告
                now = time.strftime("%Y-%m-%d %H_%M_%S")
                filename = setting.TEST_REPORTDIR + '/' + now + '_%s_result.html' % (data['testid'])
                fp = open(filename, 'wb')
                runner = HTMLTestRunner(stream=fp, title='测试报告',
                                        description='环境：windows 10 浏览器：chrome',
                                        tester='-')
                runner.run(suite)
                fp.close()
                report = new_report(setting.TEST_REPORTDIR)  # 调用模块生成最新的报告
            else:
                print("无测试用例的脚本绑定！")
            returnres['result'] = reslist
        else:
            returnres['result'] = reslist
        return jsonify(returnres)


# 前端请求接口：删除测试用例
# http://127.0.0.1:8081/api/testcase/dcase/?testid=1
@app.route('/api/testcase/dcase/')
def delexcetestcase():
    # ID
    requests = handler((dict(request.args)))  # 获取所有接收到的参数。
    error = None
    data = None
    # 反序列化
    try:
        schema = model.TestreportlistSchema()
        data = schema.load(requests)
        data = schema.dump(data)
        # print(data)
    except ValidationError as err:
        error = err.messages
        # print(error)
        # 获取数据
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    reslist = []
    if error != None:
        returnres['msg'] = error
        return jsonify(returnres)
    else:

        if 'testid' in data:
            Conn = ConnConfig()
            with Conn.engine.connect() as db:

                sql = "select test_filename,test_classname,test_funcname from " + 'tecasetable where test_id = "%s";' % (
                data['testid'])
                print(sql)
                result = db.execute(sql)
            result = result.fetchall()
            if len(result):
                pass
            else:
                print("无测试用例的脚本绑定！")
            returnres['result'] = reslist
        else:
            returnres['result'] = reslist
        return jsonify(returnres)



# 后端请求接口：执行测试用例模块
# http://127.0.0.1:8080/api/module/?file=test1API&class=UCTestCase
# http://127.0.0.1:8080/api/module/?file=test1API&class=UCTestCase,UTest1
@app.route('/api/testmodules/module/')
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


# 前端请求接口：创建任务并异步执行接口
# http://127.0.0.1:8080/api/testtask/?
@app.route('/api/testtask/')
def newexcetestmodule():
    # ID
    requests = handler((dict(request.args)))  # 获取所有接收到的参数。
    print(requests)
    error = None
    data = None
    # 反序列化
    try:
        schema = model.TaskinputSchema()
        data = schema.load(requests)
        data = schema.dump(data)
        # print(data)
    except ValidationError as err:
        error = err.messages
        print(error)
        # 获取数据
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    if error != None:
        returnres['msg'] = error
        return jsonify(returnres)
    else:
        print(data)

        if data['task_type'] == '1':
            time_temp = data['date1'] +' ' + data['date2']
            # 格式化时间转换为结构化时间
            struct_time1 = time.strptime(time_temp, '%Y-%m-%d %H-%M-%S')
            struct_time2 = time.strptime(time.strftime('%Y-%m-%d %H-%M-%S'),'%Y-%m-%d %H-%M-%S')
            print(struct_time1,struct_time2)
            time1 = time.mktime(struct_time1)
            time2 = time.mktime(struct_time2)
            # 差的时间戳
            diff_time = time1 - time2
            print(diff_time)
            if diff_time < 0:
                diff_time = 0
            print(diff_time)
            task_id =  tasks.create_timingtask.apply_async(([data]), countdown=int(diff_time))
        else:
            task_id = tasks.create_steptask.apply_async(([data]), countdown=0)
        print("task_id:",task_id)
        Conn = ConnConfig()
        with Conn.engine.connect() as db:
            if data['task_type'] == "1":
                task_context = data['date1'] + ' ' + data['date2']
            else:
                task_context = data['date3']
            sql = "select moudle_name,test_filename,test_classname from " + 'moudletable where id = %d;' % (
                data['moudleid'])
            print(sql)
            result = db.execute(sql)
            result = result.fetchall()
            sql = "insert into  tasktable(taskname,task_type,moudle_id,task_context,moudle_name,task_id) values('%s','%s','%d','%s','%s','%s');" % (
                data['task_name'], data['task_type'], data['moudleid'], task_context, result[0][0],task_id)
            print(sql)
            db.execute(sql)
    return jsonify(returnres)


# 前后端接口：获取所有的测试用例
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
            testcase = model.TestCase(id=res[0], test_pro=res[1], test_id=res[2], test_target=res[3], test_level=res[4],
                                      test_condition=res[5], test_input=res[6], test_step=res[7], test_output=res[8],
                                      is_connect=res[9], test_module=res[10])
            schema = model.TestCaseSchema()
            dumpres = schema.dump(testcase)
            reslist.append(dumpres)
        # 对序列化结果进行过滤、排序 pass
        returnres['result'] = reslist
    # print(returnres)
    return jsonify(returnres)


# 前后端接口：获取所有的任务
# http://127.0.0.1:8081/api/tetask/
@app.route('/api/tetask/')
def task():
    requests = request.args  # 获取所有接收到的参数。
    print(request.args)
    # 反序列化 pass
    # 获取数据
    Conn = ConnConfig()
    with Conn.engine.connect() as db:
        sql = "select * from tasktable;"
        result = db.execute(sql)
    result = result.fetchall()
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    reslist = []
    # 序列化
    for res in result:
        # print(res)
        testcase = model.Task(id=res[0], taskname=res[1], task_id=res[2], moudle_id=res[3], moudle_name=res[4],
                              task_type=res[5],task_context = res[6])
        schema = model.TaskSchema()
        dumpres = schema.dump(testcase)
        reslist.append(dumpres)
    # 对序列化结果进行过滤、排序 pass
    returnres['result'] = reslist
    # print(returnres)
    return jsonify(returnres)


# 前后端接口：获取所有的测试模块
# http://127.0.0.1:8081/api/temoudle/
@app.route('/api/temoudle/')
def moudle():
    requests = request.args  # 获取所有接收到的参数。
    print(request.args)
    # 反序列化 pass
    # 获取数据
    Conn = ConnConfig()
    with Conn.engine.connect() as db:
        sql = "select * from moudletable;"
        result = db.execute(sql)
    result = result.fetchall()
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    reslist = []
    # 序列化
    for res in result:
        # print(res)
        testcase = model.Moudle(id=res[0], moudle_name=res[1], test_filename=res[2], test_classname=res[3])
        schema = model.MoudleSchema()
        dumpres = schema.dump(testcase)
        reslist.append(dumpres)
    # 对序列化结果进行过滤、排序 pass
    returnres['result'] = reslist
    # print(returnres)
    return jsonify(returnres)


# 前后端接口：获取所有测试用例执行结果
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
            # print(res)
            testcase = model.TestCaseres(id=res[0], test_caseid=res[1], test_time=res[2], test_pro=res[3],
                                         test_target=res[5], test_level=res[6], test_condition=res[7],
                                         test_input=res[6], test_step=res[8], test_output=res[9], test_module=res[10])
            schema = model.TestCaseresSchema()
            dumpres = schema.dump(testcase)
            reslist.append(dumpres)
        # 对序列化结果进行过滤、排序 pass
        returnres['result'] = reslist
    # print(returnres)
    return jsonify(returnres)


# 获取某个测试用例执行报告
# http://127.0.0.1:8081/api/report/?reportname=2020-11-02 11_28_21ST-121_result.html
@app.route('/api/report/')
def testreport():
    requests = request.args  # 获取所有接收到的参数。
    print(requests.get('reportname'))
    reportname = requests.get('reportname')
    return render_template('%s' % reportname)


# 获取测试用例报告列表
# http://127.0.0.1:8081/api/reportlist/?testid=ST
@app.route('/api/reportlist/')
def testreportlist():
    # ID
    requests = handler((dict(request.args)))  # 获取所有接收到的参数。
    error = None
    data = None
    # 反序列化
    try:
        schema = model.TestreportlistSchema()
        data = schema.load(requests)
        data = schema.dump(data)
        # print(data)
    except ValidationError as err:
        error = err.messages
        # print(error)
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    reslist = []
    if error != None:
        returnres['msg'] = error
        return jsonify(returnres)
    else:
        if 'testid' in data:
            for files in os.listdir(setting.TEST_REPORTDIR):
                if data['testid'] in files:
                    reslist.append(files)
                    print(files)
            returnres['result'] = reslist
        else:
            for files in os.listdir(setting.TEST_REPORTDIR):
                reslist.append(files)
                print(files)
            returnres['result'] = reslist
        return jsonify(returnres)


# http://127.0.0.1:8081/api/test/
@app.route('/api/test/')
def test():
    tasks.add.apply_async((3, 3),countdown = 10)
    return ""


def dynamicimport(filename, clasname):
    # 动态导入包
    moud = importlib.import_module('testcase.%s' % filename, package='testcase')
    # 实例化类
    clas = getattr(moud, clasname)
    return moud, clas

def handler(requests):
    for i in requests:
        if requests[i][0]:
            requests[i] = requests[i][0]
        else:
            requests[i] = ""
    print("解析请求参数:", requests)
    return requests

# 获取图表数据
# http://127.0.0.1:8081/api/chartdata1/
@app.route('/api/chartdata1/')
def chartdata1():
    returnres = {"state": 200, "msg": "succsuful", "data": ""}
    reslist = [{'name':'springboot','value':1000},{'name':'vue','value':800}]
    resdict = {'videoData': reslist}
    returnres["data"] = resdict
    return jsonify(returnres)


# 获取图表数据
# http://127.0.0.1:80821/api/chartdata2/?xx=
@app.route('/api/chartdata2/')
def chartdata2():
    returnres = {"state": 200, "msg": "succsuful", "data": ""}
    reslist = [{'date': '周一', 'new': 100, 'active': 200}, {'date': '周二', 'new': 100, 'active': 200},
               {'date': '周三', 'new': 100, 'active': 200}, {'date': '周四', 'new': 100, 'active': 200},
               {'date': '周五', 'new': 100, 'active': 200}, {'date': '周六', 'new': 100, 'active': 200},
               {'date': '周日', 'new': 100, 'active': 200}]
    resdict = {'userData': reslist}
    returnres["data"] = resdict
    return jsonify(returnres)


# 获取图表数据
# http://127.0.0.1:80821/api/chartdata3/?xx=
@app.route('/api/chartdata3/')
def chartdata3():
    returnres = {"state": 200, "msg": "succsuful", "data": ""}
    datalist = []
    reslist = {'date':['20191001', '20191002', '20191003', '20191004', '20191005', '20191006', '20191007'],'data':''}
    for i in range(0,7):
      datalist.append(
          {
          'vue': random.randint(1, 500),
          'wechat': random.randint(1, 500),
          'ES6': random.randint(1, 500),
          'Redis': random.randint(1, 500),
          'React': random.randint(1, 500),
          'springboot': random.randint(1, 500)
        })
    reslist['data'] =datalist
    resdict = {'orderData': reslist}
    returnres["data"] = resdict

    return jsonify(returnres)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)
