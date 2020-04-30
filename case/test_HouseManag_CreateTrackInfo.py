# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,get_date
from common import readexcel
from config import *
from common.HouseManage import HouseManage

#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-创建房源跟进日志").dict_data()
print(testdata)

@ddt.ddt
class HouseManage_CreateTrackSale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        cls.caseid,cls.headers=HouseManage().create_houseSale()

    # 删除登记后出售的房源
    @classmethod
    def tearDownClass(cls):
        cls.caseid = cls.caseid
        cls.headers = cls.headers
        if cls.caseid > 0:
            # print(cls.caseid)
            url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
            data = {
                "caseId": cls.caseid,
                "caseType": "1",       # 1 代表出售房源
                "isSaleLease": "0",    # 是否是租售房源，1=是，0=否  默认是0
                "trackContent": "content",
                "trackType": "30"      # 30 代表删除房源
                    }
            cls.r = requests.post(url=url, json=data, headers=cls.headers)
            if cls.r.json()["errCode"] == 200:
                print("登记出售房源已成功删除")
            else:
                print("登记的房源删除失败的原因：%s",(cls.r.json()["errMsg"]))
        else:
            print("登记出售房源失败，没有出售的房源可删除")

    @ddt.data(*testdata)
    def test_create_trackInfo(self, case):
        a=json.loads(case["body"])
        if "targetTime" not in a.keys():
            case["headers"] = self.headers
            # 将caseid重新写入excel中
            a["caseId"]=self.caseid
            b=json.dumps(a)
            case.update({"body":b})
        else:
            case["headers"] = self.headers
            # 将caseid和targetTime重新写入excel中
            a["caseId"] = self.caseid
            a["targetTime"]= get_date.GetDate().get_tomorrow_date()
            b = json.dumps(a)
            case.update({"body": b})
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


if __name__ == "__main__":
     unittest.main()
