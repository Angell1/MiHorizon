﻿##  介绍
自动化接口测试平台
后端：python3 + Flask + Celery  + unittest测试框架及ddt数据驱动，采用Excel+Mysql管理测试用例等集成测试数据功能，以及使用HTMLTestRunner来生成测试报告;
前端：Vue3 + ElementUI + Bootstrap


## 解决什么问题
1、测试用例管理与模块化管理；
2、测试结果关联测试用例，并对测试结果进行可视化与表格化；
3、可设置实时与定时的测试任务；
4、测试环境管理，支持多环境配置；
5、支持生成测试假数据；


## 本地测试框架处理流程
测试框架处理过程如下：
1、调用exceltomysql接口，更新excel数据到数据库；
2、打开测试web平台（正在对接后台接口）；
3、执行有测试脚本关联的测试用例，发送请求数据，根据请求参数，向数据库查询得到对应测试用例的脚本位置，通过celery异步执行；
4、将代码执行的结果（JSON格式的数据）与Excel的值对比判断，并写入结果至指定Excel测试用例表格；
5、通过单元测试框架断言接口返回的数据，并生成测试报告，最后把生成最新的测试报告HTML文件发送指定的邮箱。

## 测试框架结构目录介绍
目录结构介绍如下：
* config/:                 系统配置文件
* database/:               测试用例模板文件
* db_fixture/:             初始化接口测试数据
* httpserver/:             后端测试平台对外提供服务
* lib/:                    程序核心模块，包含：更新excel到数据库、excel解析读写、发送邮箱、发送请求、生成最新测试报告文件
* package/:                存放第三方库包。如HTMLTestRunner，用于生成本地HTML格式测试报告
* report/:                 存储接口自动化测试报告
* testcase/:               用于编写接口自动化测试用例
* run_demo.py:             执行所有接口测试用例的测试主程序

