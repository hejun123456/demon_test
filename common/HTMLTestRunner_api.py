# coding=utf-8
# 作者：hejun


import unittest
from config import *
from BeautifulReport import BeautifulReport

# 加载所有以test开头的用例
def add_case(casepath=CASE_PATH, rule="test*.py"):
     discover = unittest.defaultTestLoader.discover(casepath,pattern=rule,)   # 定义discover方法的参数
     return discover

#执行所加载的用例，并把结果写入测试报告
def run_case(all_case, reportpath=REPORT_PATH):
     print("测试报告生成地址：%s"% reportpath)
     run=BeautifulReport(all_case)
     run.report(filename="result.html", description="用例执行情况",report_dir=reportpath)


# if __name__ == "__main__":
#      cases = add_case()
#      run_case(cases)