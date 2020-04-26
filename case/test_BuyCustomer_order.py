

import requests,json,ddt,unittest
from common import readexcel,base_api
from config import *
from common import add_clientkey_to_headers



@ddt.ddt
class BuyCustomerOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 如果有登录的话，就在这里先登录了
        cls.s = requests.session()
        header = add_clientkey_to_headers.get_clientkey()
        # print(header)
        cls.header = header

    #创建排序的客源
    testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求购（求租）-登记").dict_data()
    print(testdata)
    @ddt.data(*testdata)
    def test_Create_BuyAndRentCustomer(self,case):
        print(case)
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
        self.caseid = res_text["data"]["caseId"]
        # print(self.caseid)

        # 断言
        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

    #求购客源按照总面积排序
    data = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求购-总面积排序").dict_data()
    print(data)
    @ddt.data(*data)
    def test_buyCustomer_total_AreaOrder(self,case):
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
        self.assertEqual(check.get("houseAreaHigh"),res_text["data"]["buyCustomers"][0]["houseAreaHigh"])
        self.assertEqual(check.get("buildName"),(res_text["data"]["buyCustomers"][0]["buildName"]).strip())


    # 求购客源按照总价格排序
    data = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求购-总价格排序").dict_data()
    print(data)
    @ddt.data(*data)
    def test_buyCustomer_total_PriceOrder(self, case):
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
        self.assertEqual(check.get("housePriceHigh"), res_text["data"]["buyCustomers"][0]["housePriceHigh"])
        self.assertEqual(check.get("buildName"),(res_text["data"]["buyCustomers"][0]["buildName"]).strip())

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

    # 求租客源按照总价格排序
    data = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求租-总价格排序").dict_data()
    print(data)
    @ddt.data(*data)
    def test_rentCustomer_total_PriceOrder(self, case):
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
        self.assertEqual(check.get("housePriceHigh"),res_text["data"]["rentCustomers"][0]["housePriceHigh"])
        self.assertEqual(check.get("buildName"), (res_text["data"]["rentCustomers"][0]["buildName"]).strip())

if __name__ == '__main__':
        unittest.main()
