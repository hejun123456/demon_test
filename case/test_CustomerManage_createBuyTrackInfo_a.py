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
class CustomerManage_CreateBuyCustomerTrack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，在这里先登录
        cls.s = requests.session()
        #创建一个出售中的房源，并获取到caseid
        cls.saleHouse_caseid,cls.saleHeaders=HouseManage().create_houseSale()

        #创建一个求购客源，获取到caseid，用于后续创建跟进
        cls.caseid,cls.headers=CustomerManage().create_BuyCustomer()

    # 删除登记后的求购客源以及登记的出售房源
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

    #求购客源去电、回访和面谈跟进
    testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求购-创建跟进日志").dict_data()
    print(testdata)
    @ddt.data(*testdata)
    def test_create_buy_customer_trackInfo(self, case):
        case["headers"] = self.headers
        # 将caseid重新写入excel中
        a=json.loads(case["body"])
        a["caseId"]=self.caseid
        b=json.dumps(a)
        case.update({"body":b})
        print(case)

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
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

    # 求购客源约看
    def test_create_buyCustomer_trackInfo_yuekan(self):
        url="http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        headers = self.headers
        data={"caseId":self.caseid,
              "caseType":"3",
              "houseIds":self.saleHouse_caseid,
              "lookType":"0",
              "targetTime":get_date.GetDate().get_tomorrow_date_time("13:00"),"trackTag":"","trackType":"68"}
        res=requests.post(url,json=data,headers=headers)

        # 检查点
        check = res.json()       # 获取检查点中的内容
        print("返回实际结果->：%s" % check)

        self.makeLookId = check["data"]["makeLookId"]
        print("约看id：%s" %(self.makeLookId))
        # 断言
        self.assertEqual(200, check["errCode"])

        # 求购客源带看
        url="http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        headers = self.headers
        datas={"caseId":self.caseid,
               "caseType":"3",
               "daiKanHouseList":[{"lookType":"0","makeLookId":self.makeLookId,"targetId":self.saleHouse_caseid,"trackContent":"123456"}],
               "isImmediate":"0","targetType":"1",
               "trackType":"4","userIds":"20174961","userNames":"张小林"}

        r=requests.post(url,json=datas,headers=headers)

        # 检查点
        check = r.json()       # 将返回值转换成字典数据类型
        print("带看后返回实际结果->：%s" % check)
        # 断言
        self.assertEqual(200, check["errCode"])

        #求购客源面谈
        url="http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        headers=self.headers
        data={"caseId":self.caseid,
              "caseType":"3",
              "trackContent":"客户已锁定意向房源，决策中",
              "trackType":"2"}
        rs=requests.post(url,json=data,headers=headers)
        checks=rs.json()
        print("面谈后返回实际结果->：%s" % checks)
        # 断言
        self.assertEqual(200, checks["errCode"])

        #求购客源预定
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        headers = self.headers
        data = {"caseId": self.caseid,
                "caseType": "3",
                "targetTime": get_date.GetDate().get_fengpan_date(),
                "trackContent": "客户意向强烈，已进入预定阶段",
                "trackType": "25"}
        rs = requests.post(url, json=data, headers=headers)
        checks = rs.json()
        print("客源预定后返回实际结果->：%s" % checks)
        # 断言
        self.assertEqual(200, checks["errCode"])


if __name__ == "__main__":
     unittest.main()
