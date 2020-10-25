from flask import Flask,request
import importlib
import unittest
import inspect


# http://127.0.0.1:8080/testcase/?file=test1API&class=UCTestCase&func=testCreateFolder
app = Flask(__name__)
@app.route('/testcase/')
def testcase():
    requests = request.args  # 获取所有接收到的参数。
    print(requests.get('file'))
    filename = requests.get('file')
    print(requests.get('class'))
    clasname = requests.get('class')
    print(requests.get('func'))
    funcname = requests.get('func')
    moud,clas = dynamicimport(filename,clasname)

    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(clas(funcname))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    return '<h1>Hello World!</h1>'



# http://127.0.0.1:8080/testmould/?file=test1API&class=UCTestCase
# http://127.0.0.1:8080/testmould/?file=test1API&class=UCTestCase,UTest1
@app.route('/testmould/')
def testmould():
    requests = request.args  # 获取所有接收到的参数。
    print(requests.get('file'))
    filename = requests.get('file')
    print(requests.get('class'))
    clasname = requests.get('class')
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
    return '<h1>Hello World!</h1>'


def dynamicimport(filename,clasname):
    # 动态导入包
    moud = importlib.import_module('testcase.%s' % filename, package='testcase')
    # 实例化类
    clas = getattr(moud, clasname)

    return moud,clas



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080,debug=True)