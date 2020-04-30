# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,HouseManage,get_date
from common import readexcel
from config import *



#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-委托").dict_data()
print(testdata)

@ddt.ddt
class TestHouseManager(unittest.TestCase):
    def setUp(self):
        # 如果有登录的话，就在这里先登录了
        self.s = requests.session()
        self.caseid,self.header=HouseManage.HouseManage().create_houseSale()
    def tearDown(self):
        salehouse_code=HouseManage.HouseManage().delete_houseSale(self.caseid)
        if salehouse_code==200:
            print("出售房源删除成功")
    @ddt.data(*testdata)
    def test_add_entrust(self, case):
        a=json.loads(case["body"])
        if len(a["caseId"])==0:
            case["headers"]=self.header
            a["targetTime"]=get_date.GetDate().get_tomorrow_date()
            b=json.dumps(a)
            case.update({"body":b})
        else:
            a["caseId"]=self.caseid
            case["headers"] = self.header
            a["targetTime"] = get_date.GetDate().get_tomorrow_date()
            b = json.dumps(a)
            case.update({"body": b})

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

if __name__ == "__main__":
     unittest.main()
