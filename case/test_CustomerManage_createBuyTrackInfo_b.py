# coding:utf-8
# 作者：hejun

import unittest
import ddt
import requests,json
from common import base_api,get_date
from common import readexcel
from config import *
from common.HouseManage import HouseManage
from common.CustomerManage import CustomerManage

@ddt.ddt
class CustomerManage_CreateBuyCustomerTrack_FengPanAndZanHuan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，在这里先登录
        cls.s = requests.session()
        #创建一个出售中的房源，并获取到caseid
        cls.saleHouse_caseid,cls.saleHeaders=HouseManage().create_houseSale()

        #创建一个求购客源，获取到caseid，用于后续创建跟进
        cls.caseid,cls.headers=CustomerManage().create_BuyCustomer()

    # 删除登记后的求购客源以及登记的房源
    @classmethod
    def tearDownClass(cls):
        cls.caseid = cls.caseid
        cls.headers = cls.headers
        cls.saleHouse_caseid = cls.saleHouse_caseid
        #删除求购客源
        if cls.caseid > 0:
            # print(cls.caseid)
            url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
            data = {
                "caseId": cls.caseid,
                "caseType": "3",       # 3 代表求购客源
                "isSaleLease": "0",    # 是否是租售房源，1=是，0=否  默认是0
                "trackContent": "content",
                "trackType": "30"      # 30 代表删除客源信息
                    }
            cls.res = requests.post(url=url, json=data, headers=cls.headers)
            if cls.res.json()["errCode"] == 200:
                print("登记求购客源已成功删除")
            else:
                print("登记的求购客源删除失败的原因：%s",(cls.res.json()["errMsg"]))
        else:
            print("登记求购的客源删除失败，没有登记的求购客源可删除")

        #删除登记的出售房源
        if cls.saleHouse_caseid > 0:
            # print(cls.caseid)
            url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
            data = {
                "caseId": cls.saleHouse_caseid,
                "caseType": "1",       # 1 代表出售房源
                "isSaleLease": "0",    # 是否是租售房源，1=是，0=否  默认是0
                "trackContent": "content",
                "trackType": "30"      # 30 代表删除客源信息
                    }
            cls.r = requests.post(url=url, json=data, headers=cls.headers)
            if cls.r.json()["errCode"] == 200:
                print("登记出售房源已成功删除")
            else:
                print("登记出售房源删除失败的原因：%s",(cls.r.json()["errMsg"]))
        else:
            print("登记出售房源删除失败，没有登记的出售房源可删除")
    # 求购客源封盘跟进日志
    testdatas = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求购-创建封盘跟进").dict_data()
    print(testdatas)
    @ddt.data(*testdatas)
    def test_create_buy_customer_fengpan_trackInfo(self, cases):
        a=json.loads(cases["body"])
        if "targetTime" in a.keys():
            cases["headers"] = self.headers
            # 将caseid重新写入excel中
            a["caseId"] = self.caseid
            a["targetTime"] = get_date.GetDate().get_fengpan_date()
            b = json.dumps(a)
            cases.update({"body": b})
        else:
            cases["headers"] = self.headers
            # 将caseid重新写入excel中
            a["caseId"] = self.caseid
            b = json.dumps(a)
            cases.update({"body": b})

        res = base_api.send_requests(self.s, cases)

        # 检查点 checkpoint
        check = cases["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        # 断言
        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

    # 求购客源暂缓跟进日志
    test_data = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求购-创建暂缓跟进").dict_data()
    print(test_data)
    @ddt.data(*test_data)
    def test_create_buy_customer_zanhuan_trackInfo(self, data):
        a=json.loads(data["body"])
        if "targetTime" in a.keys():
            data["headers"] = self.headers
            # 将caseid重新写入excel中
            a["caseId"] = self.caseid
            a["targetTime"] = get_date.GetDate().get_zanhuan_date()
            b = json.dumps(a)
            data.update({"body": b})
            print(data)
        else:
            data["headers"] = self.headers
            # 将caseid重新写入excel中
            a["caseId"] = self.caseid
            b = json.dumps(a)
            data.update({"body": b})
            print(data)

        res = base_api.send_requests(self.s, data)

        # 检查点 checkpoint
        check = data["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        # 断言
        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

if __name__ == "__main__":
     unittest.main()
