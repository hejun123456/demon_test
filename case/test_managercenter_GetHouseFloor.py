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
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="管理中心-获取楼盘信息").dict_data()
print(testdata)

@ddt.ddt
class TestGetHouseFloor(unittest.TestCase):
    # def __init__(self):
    #     super().__init__()
    #     self.headers = {}
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        # print(header)
        cls.header = header

    @ddt.data(*testdata)
    def test_getHouseFloor(self, testdata):
        testdata["headers"]=self.header
        # print(self.header)

        # aes_util=AesHelper()
        # testdata["body"]=aes_util.encrypt(testdata["body"])
        # print(testdata["body"])

        res = base_api.send_requests(self.s,testdata)

        # 检查点 checkpoint
        check = testdata["checkpoint"]  #获取检查点中的内容
        check=json.loads(check)         #字符串转为字典
        print("检查点->：%s" % check)



        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)

        # 断言

        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("buildName"),res_text["data"]["buildInfoVOS"][0]["buildName"])

        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])




if __name__ == "__main__":
     unittest.main()
