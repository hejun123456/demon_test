

import requests,json,ddt,unittest
from common import readexcel,base_api,CustomerManage
from config import *

@ddt.ddt
class BuyCustomerOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        #创建求租中按照面积来排序的房源
        cls.Lower_caseid=CustomerManage.CustomerManage().create_RentCustomer_LowerArea()
        cls.High_caseid,cls.header=CustomerManage.CustomerManage().create_RentCustomer_HighArea()

    @classmethod
    def tearDownClass(cls):
        lower_coed=CustomerManage.CustomerManage().delete_rentCustomer(cls.Lower_caseid)
        high_code=CustomerManage.CustomerManage().delete_rentCustomer(cls.High_caseid)

        if lower_coed == 200 and high_code == 200:
            print("房源删除成功")
        else:
            print("房源删除失败")


    # 求租客源按照总面积排序
    data = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求租-总面积排序").dict_data()
    print(data)
    @ddt.data(*data)
    def test_rentCustomer_total_AreaOrder(self, case):
        case["headers"] = self.header
        res = base_api.send_requests(self.s, case)
        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        # 断言
        self.assertEqual(check.get("houseAreaHigh"), res_text["data"]["rentCustomers"][0]["houseAreaHigh"])
        self.assertEqual(check.get("buildName"), (res_text["data"]["rentCustomers"][0]["buildName"]).strip())


if __name__ == '__main__':
        unittest.main()
