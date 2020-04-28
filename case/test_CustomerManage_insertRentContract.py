# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,CustomerManage,HouseManage,get_date
from common import readexcel
from config import *


#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH,sheetName="客源管理-求租-新增合同").dict_data()
print(testdata)
@ddt.ddt
class CustomerManage_InsertBuyContract(unittest.TestCase):
    def setUp(self):
        # 保持会话状态
        self.s = requests.session()
        #登记出租房源并获取房源id
        self.lease_caseid,self.lease_header = HouseManage.HouseManage().create_houseLease()
        #登记求租客源并获取客源id
        self.caseid,self.header=CustomerManage.CustomerManage().create_RentCustomer()
        # 获取出租中未使用的合同编号
        self.codeNo,self.headers = CustomerManage.CustomerManage().get_rentMatchNotAllocatedDealCode()

    #删除登记后的求租客源以及出租中的房源
    def tearDown(self):
        if self.caseid > 0:
            buyCustomer_errcode=CustomerManage.CustomerManage().delete_rentCustomer(self.caseid)
            if buyCustomer_errcode == 200:
                print("登记求租的客源已成功删除")
        else:
            print("登记求租客源删除失败")
        # 删除登记的出租房源
        if self.lease_caseid > 0:
            huoseSale_errcode = HouseManage.HouseManage().delete_leaseHouse(self.lease_caseid)
            if huoseSale_errcode == 200:
                print("登记出租房源已成功删除")
        else:
            print("登记出租房源删除失败")

    @ddt.data(*testdata)
    def test_insertContract_rentCustomer(self, case):
        if "dealHouseId" not in case.keys():
            case["headers"]=self.headers
            a = json.loads(case["body"])
            a["custId"] = self.caseid
            a["dealCustomerId"] = self.caseid
            a["rentDate"]=get_date.GetDate().get_today_str_data()
            a["rentOverDate"] = get_date.GetDate().get_zanhuan_date()
            a["contractNo"]=self.codeNo
            b = json.dumps(a)
            case.update({"body": b})
        else:
            case["headers"] = self.headers
            a = json.loads(case["body"])
            a["custId"] = self.caseid
            a["dealCustomerId"] = self.caseid
            a["signDate"] = get_date.GetDate().get_today_str_data()
            a["rentOverDate"] = get_date.GetDate().get_zanhuan_date()
            a["contractNo"] = self.codeNo
            a["dealHouseId"] = self.lease_caseid
            a["houseId"] = self.lease_caseid

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
