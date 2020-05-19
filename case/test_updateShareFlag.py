# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api
from common import readexcel
from config import *
from common.HouseManage import HouseManage
from common import addimage
from common import add_clientkey_to_headers

jpgpath=JPG_PATH

testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-点亮合作房源").dict_data()
print(testdata)

@ddt.ddt
class UpdateShareFlag(unittest.TestCase):

    def setUp(self):
        self.s = requests.session()
        # 创建出售房源
        self.caseid,self.header = HouseManage().create_houseSale()

        # 上传3张图片
        url = "http://hft.myfun7.com/houseWeb/housePhoto/createMultipleHousePhotos"
        data = {"caseId": self.caseid, "caseType": "1",
                "photoAddr": addimage.AddImg().sendImg(jpgpath)+","+addimage.AddImg().sendImg(jpgpath)+","+addimage.AddImg().sendImg(jpgpath),
                "photoSource": "1", "photoType": "0"}
        self.headers=add_clientkey_to_headers.get_clientkey()       # 重新获取clientkey
        res = requests.post(url, json=data, headers=self.headers)
        print(res.json())

    def tearDown(self):
        # 删除该房源
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
                "caseId": self.caseid,
                "caseType": "1",        # 1 代表出售房源
                "isSaleLease": "0",     # 是否是租售房源，1=是，0=否  默认是0
                "trackContent": "content",
                "trackType": "30"       # 30 代表删除房源
                }
        r = requests.post(url=url, json=data, headers=self.headers)

        if r.json()["errCode"] == 200:
            print("登记出售房源已成功删除")
        else:
            print("登记的房源删除失败的原因：%s", (r.json()["errMsg"]))

    @ddt.data(*testdata)
    def test_updateShareFlag(self, case):
        case["headers"]=self.headers
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
        if "cooperateRatio" in check.keys():
            self.assertEqual(check.get("cooperateRatio"),res_text["data"]["cooperateRatio"])
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"),res_text["errMsg"])
if __name__ == "__main__":
     unittest.main()