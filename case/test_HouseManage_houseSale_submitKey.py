# coding:utf-8
# 作者：hejun


import unittest,ddt,time
import requests,json
from common import base_api,HouseManage
from common import readexcel
from config import *



#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-提交钥匙").dict_data()
print(testdata)

@ddt.ddt
class TestHouseManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        cls.caseid,cls.header=HouseManage.HouseManage().create_houseSale()
    @classmethod
    def tearDownClass(cls):
        code=HouseManage.HouseManage().delete_houseSale(cls.caseid)
        if code==200:
            print("登记出售房源删除成功")
    @ddt.data(*testdata)
    def test_houseSale_submit_key(self, testdata):
        testdata["headers"]=self.header
        a=json.loads(testdata["body"])
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
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])
        time.sleep(5)
if __name__ == "__main__":
     unittest.main()
