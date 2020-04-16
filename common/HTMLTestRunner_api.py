# coding=utf-8
# 作者：hejun


import unittest
import HTMLTestRunner
from config import *


def add_case(casepath=CASE_PATH, rule="test*.py"):
     '''加载所有的测试用例'''
     # 定义discover方法的参数
     discover = unittest.defaultTestLoader.discover(casepath,pattern=rule,)
     return discover

def run_case(all_case, reportpath=REPORT_PATH):
     '''执行所有的用例, 并把结果写入测试报告'''
     htmlreport = reportpath+r"\result.html"
     print("测试报告生成地址：%s"% htmlreport)
     with open(htmlreport, "wb") as f:
        runner=HTMLTestRunner.HTMLTestRunner(stream=f,verbosity=2,title="测试报告", description="用例执行情况")
        runner.run(all_case)


# if __name__ == "__main__":
#      cases = add_case()
#      run_case(cases)