# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api
from common import readexcel
from config import *
from common import add_clientkey_to_headers
from common.HouseManage import HouseManage
from common.fileupload import TestSendFile



testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-笋盘").dict_data()
print(testdata)

@ddt.ddt
class SunPan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        housemanage=HouseManage()
        cls.caseid,cls.header=housemanage.create_houseSale()
        #房堪
        url="http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data={"caseId":cls.caseid,"caseType":"1","coreSellPoint":"好","trackContent":"核心卖点：好","trackType":"3"}

        requests.post(url,json=data,headers=cls.header)

        #上传5张房勘图片
        url="http://hft.myfun7.com/houseWeb/housePhoto/createMultipleHousePhotos"
        data={"caseId":cls.caseid,"caseType":"1","photoAddr":"oss/online/tmp/2020/04/23/c19456a8739042fda065b2d7fbe69049.jpg,oss/online/tmp/2020/04/23/6cf18050393d4fcbad3b2101fe9bc4d6.jpg,oss/online/tmp/2020/04/23/f075f9f72c43464fa0f78cb7e8d08b22.jpg,oss/online/tmp/2020/04/23/cb82a2c0834e403cb2e419aed3d399b5.jpg,oss/online/tmp/2020/04/23/62ab76105de54c94b337b583137da9e8.jpg","photoSource":"1","photoType":"0"}
        res=requests.post(url,json=data,headers=cls.header)
        print("111111")
        print(res.json())

        #查看房源笋盘剩余推送条数
        url="http://hft.myfun7.com/houseWeb/houseCust/getFocusPlateCount"
        data={"caseId":cls.caseid,"caseType":"1"}
        res=requests.post(url,json=data,headers=cls.header)
        print(res.json())

    #创建笋盘
    @ddt.data(*testdata)
    def test_sunpan(self, case):
        case["headers"] = self.header
        a = json.loads(case["body"])
        a["caseId"] = self.caseid
        b = json.dumps(a)
        case.update({"body": b})

        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # 字符串转为字典
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

    #取消笋盘及删除房源
    @classmethod
    def tearDownClass(cls):
        cls.caseid=cls.caseid
        cls.header=cls.header
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": cls.caseid,
            "caseType": "1",  # 1 代表出售房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content2132323",
            "trackType": "81"  # 81 代表取消笋盘
                }
        r = requests.post(url, json=data, headers=cls.header)
        r.json()["errCode"] = 200
        print("取消笋盘成功")

        #删除该房源
        headers=cls.header
        deleurl = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": cls.caseid,
            "caseType": "1",  # 1 代表出售房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "30"  # 30 代表删除房源
                }
        cls.r = requests.post(url=deleurl, json=data, headers=headers)
        # print(cls.r.text)
        if cls.r.json()["errCode"] == 200:
            print("登记出售房源已成功删除")
        else:
            print("登记的房源删除失败的原因：%s", (cls.r.json()["errMsg"]))


if __name__ == "__main__":
     unittest.main()
