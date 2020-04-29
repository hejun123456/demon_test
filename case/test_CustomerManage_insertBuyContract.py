# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,CustomerManage,HouseManage,get_date
from common import readexcel
from config import *


#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH,sheetName="客源管理-求购-新增合同").dict_data()
print(testdata)
@ddt.ddt
class CustomerManage_InsertBuyContract(unittest.TestCase):
    def setUp(self):
        # 保持会话状态
        self.s = requests.session()
        #登记出售房源并获取房源id
        self.sale_caseid,self.sale_header = HouseManage.HouseManage().create_houseSale()
        #登记求购客源并获取id
        self.caseid,self.header=CustomerManage.CustomerManage().create_BuyCustomer()
        # 获取出售中未使用的合同编号
        self.codeNo,self.headers = CustomerManage.CustomerManage().get_buyMatchNotAllocatedDealCode()

    #删除登记后的求购客源以及出售中的房源
    def tearDown(self):
        if self.caseid > 0:
            buyCustomer_errcode=CustomerManage.CustomerManage().delete_buyCustomer(self.caseid)
            if buyCustomer_errcode == 200:
                print("登记求购的客源已成功删除")
        else:
            print("登记求购客源删除失败")
        # 删除登记的出售房源
        if self.sale_caseid > 0:
            huoseSale_errcode = HouseManage.HouseManage().delete_houseSale(self.sale_caseid)
            if huoseSale_errcode == 200:
                print("登记出售房源已成功删除")
        else:
            print("登记出售房源删除失败")

    @ddt.data(*testdata)
    def test_insertContract_buyCustomer(self, case):
        a=json.loads(case["body"])
        if "dealHouseId" not in a.keys():
            case["headers"]=self.headers
            a["custId"] = self.caseid
            a["dealCustomerId"] = self.caseid
            a["signDate"]=get_date.GetDate().get_today_str_data()
            a["contractNo"]=self.codeNo
            b = json.dumps(a)
            case.update({"body": b})
        else:
            case["headers"] = self.headers
            a["custId"] = self.caseid
            a["dealCustomerId"] = self.caseid
            a["signDate"] = get_date.GetDate().get_today_str_data()
            a["contractNo"] = self.codeNo
            a["dealHouseId"] = self.sale_caseid
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
        self.dealId=res_text["data"]["dealId"]

        # 断言
        if "errMsg" not in res_text.keys() and self.dealId > 0:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

if __name__ == "__main__":
     unittest.main()

