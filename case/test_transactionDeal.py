# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,CustomerManage,HouseManage,TransactionDeal
from common import readexcel
from config import *


#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-审核合同").dict_data()
print(testdata)
@ddt.ddt
class TestTransactionDeal(unittest.TestCase):
    def setUp(self):
        # 保持会话状态
        self.s = requests.session()
        self.deal_id, self.header, self.sale_id, self.custor_id = TransactionDeal.TransactionDeal().create_transaction_deal()


    #删除登记后的求购客源以及出售中的房源
    # def tearDown(self):
    #     if self.caseid > 0:
    #         buyCustomer_errcode = CustomerManage.CustomerManage().delete_buyCustomer(self.custor_id)
    #         if buyCustomer_errcode == 200:
    #             print("登记求购的客源已成功删除")
    #     else:
    #         print("登记求购客源删除失败")
    #     # 删除登记的出售房源
    #     if self.sale_caseid > 0:
    #         huoseSale_errcode = HouseManage.HouseManage().delete_houseSale(self.sale_id)
    #         if huoseSale_errcode == 200:
    #             print("登记出售房源已成功删除")
    #     else:
    #         print("登记出售房源删除失败")

    @ddt.data(*testdata)
    def test_insertContract_buyCustomer(self, case):
        a=json.loads(case["body"])
        case["headers"] = self.header
        a["dealId"] = self.deal_id
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
        if "errMsg" not in check.keys():
            self.assertEqual(check.get("errCode"), res_text["errCode"])

        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("needAudit"), res_text["data"]["needAudit"])

if __name__ == "__main__":
     unittest.main()

