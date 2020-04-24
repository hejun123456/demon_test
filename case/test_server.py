# coding:utf-8
# 作者：hejun


import unittest
import ddt
import os
import requests
from common import base_api
from common import readexcel
from common import writeexcel
from config import *



#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="服务器接口").dict_data()

@ddt.ddt
class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()

         # 先复制excel数据到report
         # writeexcel.copy_excel(EXCEL_PATH, RESULT_PATH)

    @ddt.data(*testdata)
    def test_server(self, testdata):

        res = base_api.send_requests(self.s,testdata)
        # base_api.wirte_result(res, filename=RESULT_PATH)

        # 检查点 checkpoint
        check = testdata["checkpoint"]
        print("检查点->：%s"%check)

        # 返回结果
        res_text = res["text"]
        print("返回实际结果->：%s"%res_text)

        # 断言
        self.assertTrue(check in res_text)


if __name__ == "__main__":
     unittest.main()