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
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-登记").dict_data()
print(testdata)

@ddt.ddt
class HouseManage_HouseSale(unittest.TestCase):
    # @classmethod
    def setUp(self):
        # 如果有登录的话，就在这里先登录了
        self.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        self.header=header

    @ddt.data(*testdata)
    def test_create_houseSale(self, case):
        case["headers"]=self.header

        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]      #获取检查点中的内容
        check=json.loads(check)         #json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)
        datas=res_text["data"]

        #删除登记后的房源
        if "caseId" in datas.keys():
            self.caseid=res_text["data"]["caseId"]
            errCode = HouseManage.HouseManage().delete_houseSale(self.caseid)
            if errCode == 200:
                print("登记出售房源已成功删除")
                #断言
                self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            print("出售房源登记失败errMsg:%s" % (res_text["errMsg"]))
            #断言
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])


if __name__ == "__main__":
     unittest.main()
