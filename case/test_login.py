# coding:utf-8
# 作者：hejun
import json
import unittest
import ddt
import requests

from aes_c import aes_util
from common import base_api
from common import readexcel
from config import *

# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="登录接口").dict_data()
print(testdata)

@ddt.ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()

    @ddt.data(*testdata)
    def test_login(self, case):
        # case = json.dumps(case)
        # case = aes_util.encrypt(case)
        res = base_api.send_requests(self.s, case)
        # base_api.wirte_result(res, filename=RESULT_PATH)

        # 检查点 checkpoint
        check = case["checkpoint"]
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]
        print("返回实际结果->：%s" % res_text)

        # 断言
        self.assertTrue(check in res_text)


if __name__ == "__main__":
    unittest.main()
