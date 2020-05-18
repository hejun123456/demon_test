# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,get_date
from common import readexcel,addimage,login_get_clientkey
from config import *
from common.HouseManage import HouseManage

#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-视频上传").dict_data()
print(testdata)

@ddt.ddt
class HouseManage_saleHouse_videoUpload(unittest.TestCase):

    def setUp(self):
        # 如果有登录的话，就在这里先登录了
        self.s = requests.session()

        #获取上传视频的url
        login_get_clientkey.login()
        self.video_url = addimage.AddImg().sendVide(VIDEO_PATH)

        #创建出售的房源
        self.caseid,self.headers=HouseManage().create_houseSale()


    # 删除登记后出售的房源
    def tearDown(self):
        # 删除视频
        if "videoId" in self.res_text.keys():
            code=HouseManage().delete_saleHouse_video(self.headers,self.caseid,self.res_text["videoId"])
            if code==200:
                print("视频成功删除")
            else:
                print("视频删除失败")

        #删除房源
        if self.caseid > 0:
            # print(cls.caseid)
            url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
            data = {
                "caseId": self.caseid,
                "caseType": "1",       # 1 代表出售房源
                "isSaleLease": "0",    # 是否是租售房源，1=是，0=否  默认是0
                "trackContent": "content",
                "trackType": "30"      # 30 代表删除房源
                    }
            r = requests.post(url=url, json=data, headers=self.headers)
            if r.json()["errCode"] == 200:
                print("登记出售房源已成功删除")
            else:
                print("登记的房源删除失败的原因：%s",(r.json()["errMsg"]))
        else:
            print("登记出售房源失败，没有出售的房源可删除")

    @ddt.data(*testdata)
    def test_saleHouse_uploadVideo(self, case):
        case["headers"] = self.headers
        a=json.loads(case["body"])
        if a["caseId"] != "":
            # 将caseid以及video_url重新写入excel中
            a["caseId"]=self.caseid
            a["videoAddr"]=self.video_url
            b=json.dumps(a)
            case.update({"body":b})
        else:
            pass
        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]      #获取检查点中的内容
        check=json.loads(check)         #json字符串转为字典
        print("检查点->：%s" % check)


        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)
        self.res_text = res_text["data"]

        # 断言
        if "videoAddr" and "photoAddr" in check.keys():
            check["videoAddr"] = res_text["data"]["videoAddr"]      # 将返回的videoAddr写入到检测点中去，方便后面的断言
            check["photoAddr"] = res_text["data"]["photoAddr"]      # 将返回的photoAddr写入到检测点中去，方便后面的断言
            # 断言
            self.assertEqual(check.get("videoAddr"), res_text["data"]["videoAddr"])
            self.assertEqual(check.get("photoAddr"), res_text["data"]["photoAddr"])
            self.assertEqual(check.get("errCode"),res_text["errCode"])

        elif "videoAddr" in check.keys():
            check["videoAddr"] = res_text["data"]["videoAddr"]
            self.assertEqual(check.get("videoAddr"), res_text["data"]["videoAddr"])
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        elif check.get("nullvideoAddr") == "nullhttp":
            self.assertIn("nullhttp", res_text["data"]["videoAddr"])
        else:
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])
            self.assertEqual(check.get("errCode"), res_text["errCode"])


if __name__ == "__main__":
     unittest.main()