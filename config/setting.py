#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = '-零'

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)
sys.path.append(BASE_DIR)

# 项目配置文件
TEST_CONFIG =  os.path.join(BASE_DIR,"config","config.ini")
# 测试用例模板目录
SOURCE_DIR = os.path.join(BASE_DIR,"database")
# 测试用例模板文件
SOURCE_FILE = os.path.join(BASE_DIR,"database","DemoAPITestCase.xlsx")
# excel测试用例结果目录
# TARGET_DIR = os.path.join(BASE_DIR,"report","excelReport")
# 测试报告
TEST_REPORTDIR = os.path.join(BASE_DIR,"httpserver",'src','templates')
