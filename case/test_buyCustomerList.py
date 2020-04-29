# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api
from common import readexcel
from config import *
from common import add_clientkey_to_headers


#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH,sheetName="客源管理-求购-获取求购列表").dict_data()
print(testdata)

@ddt.ddt
class CustomerManage_GetBuyCustomerList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持会话状态
        cls.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        cls.header = header


    @ddt.data(*testdata)
    def test_getBuyCustomerList(self, case):
        case["headers"]=self.header

        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]      #获取检查点中的内容
        check=json.loads(check)         #json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)


        # 断言
        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("code"), res_text["code"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

if __name__ == "__main__":
     unittest.main()
