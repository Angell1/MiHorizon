import unittest

a = 0
# 执行测试的类
class UCTestCase(unittest.TestCase):
    def setUp(self):
        pass
        # 测试前需执行的操作


    def tearDown(self):
        pass

    # 测试用例1
    def testCreateFolder(self):
        # 具体的测试脚本
        print(1)
        pass
        # 测试用例2

    def testDeleteFolder(self):
        print(2)
        # 具体的测试脚本
        pass
# 执行测试的类
class UTest1(unittest.TestCase):
    def setUp(self):
        pass
        # 测试前需执行的操作


    def tearDown(self):
        pass

    # 测试用例1
    def testCreateFolder(self):
        # 具体的测试脚本
        print(3)
        pass
        # 测试用例2

    def testDeleteFolder(self):
        print(4)
        # 具体的测试脚本
        pass

if __name__ == "__main__":
    pass