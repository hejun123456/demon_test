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
testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH,sheetName="客源管理-求购-登记").dict_data()
print(testdata)

@ddt.ddt
class CustomerManage_BuyCustomer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        # print(header)
        cls.header = header

    #删除登记后的客源
    def tearDown(self):
        if self.caseid > 0:
            url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
            data = {
                    "caseId": self.caseid,
                    "caseType": "3",         # 3 代表求购客源
                    "trackContent": "content",
                    "trackType": "30"        # 30 代表删除房源
                }
            r = requests.post(url=url, json=data, headers=self.header)
            # print(r.json()["errCode"])
            self.assertEqual(200, r.json()["errCode"])
            print("登记出售房源已成功删除")
        else:
            print("登记出售房源失败，没有出售的房源可删除")

    @ddt.data(*testdata)
    def test_create_buyCustomer(self, case):
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
        self.caseid=res_text["data"]["caseId"]
        # print(self.caseid)

        # 断言
        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

if __name__ == "__main__":
     unittest.main()
