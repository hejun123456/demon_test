# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,HouseManage
from common import readexcel
from config import *
from common import add_clientkey_to_headers




#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-获取钥匙信息").dict_data()
print(testdata)

@ddt.ddt
class TestHouseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        #登记一套出售房源
        cls.caseid,cls.a=HouseManage.HouseManage().create_houseSale()
        #提交钥匙到一套房源
        cls.headers=HouseManage.HouseManage().submitKey_houseSale(cls.caseid)
    @classmethod
    def tearDownClass(cls) -> None:
        code=HouseManage.HouseManage().delete_houseSale(cls.caseid)
        if code==200:
            print("出售房源删除成功")
        else:
            print("出售房源删除失败")
    @ddt.data(*testdata)
    def test_getKeyInfo(self, testdata):
        a=json.loads(testdata["body"])
        if a["caseId"] == "":
            testdata["headers"]=self.headers
        else:
            testdata["headers"] = self.headers
            a["caseId"]=self.caseid
            b=json.dumps(a)
            testdata.update({"body":b})
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
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertTrue(len(res_text["data"]["keyNum"]) > 0)
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

# if __name__ == "__main__":
#      unittest.main()
