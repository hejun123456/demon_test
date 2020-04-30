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
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-房堪").dict_data()
print(testdata)

@ddt.ddt
class TestHouseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持会话状态如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        #创建一个出售房源
        cls.caseid,cls.header=HouseManage.HouseManage().create_houseSale()
    @classmethod
    def tearDownClass(cls):
        errcode=HouseManage.HouseManage().delete_houseSale(cls.caseid)
        if errcode==200:
            print("登记的出售房源删除成功")
        else:
            print("房源删除失败")
    @ddt.data(*testdata)
    def test_house_cust(self, case):
        case["headers"]=self.header
        a=json.loads(case["body"])
        a["caseId"] = self.caseid
        b=json.dumps(a)
        case.update({"body":b})
        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]  #获取检查点中的内容
        check=json.loads(check)         #字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)


        # 断言

        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

# if __name__ == "__main__":
#      unittest.main()
