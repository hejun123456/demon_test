# coding:utf-8
# 作者：hejun



import unittest
import ddt
import requests,json
from common import base_api,CustomerManage,get_date
from common import readexcel,add_clientkey_to_headers
from config import *



#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH,sheetName="获取出售和出租未领用的合同列表").dict_data()
print(testdata)
@ddt.ddt
class MatchNotAllocatedDealCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        #获取clientkey
        cls.headers = add_clientkey_to_headers.get_clientkey()

    @ddt.data(*testdata)
    def test_matchNotAllocatedDealCode(self,case):
        case["headers"]=self.headers
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
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("codeId"),res_text["data"]["list"][0]["codeId"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

if __name__ == "__main__":
     unittest.main()
