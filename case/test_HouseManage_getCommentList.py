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
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-查询房源点评表").dict_data()
print(testdata)

@ddt.ddt
class TestHouseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        cls.sale_caseid,cls.sale_header=HouseManage.HouseManage().create_houseSale()
    @classmethod
    def tearDownClass(cls):
        sale_code=HouseManage.HouseManage().delete_houseSale(cls.sale_caseid)
        if sale_code==200:
            print("出售房源成功删除")
        else:
            print("房源删除失败")
    @ddt.data(*testdata)
    def test_get_comment_list(self, testdata):
        a=json.loads(testdata["body"])
        if a["caseId"]=="":
            testdata["headers"]=self.sale_header
        else:
            testdata["headers"]=self.sale_header
            a["caseId"]=self.sale_caseid
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
        if res_text["data"]["commentList"]==[]:
            self.assertEqual(check.get("commentList"),res_text["data"]["commentList"])
        else:
            self.assertEqual(check.get("coreInfo"),res_text["data"]["commentList"][0]["coreInfo"])


if __name__ == "__main__":
     unittest.main()
