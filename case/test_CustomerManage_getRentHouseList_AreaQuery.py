

import unittest,json,ddt
from common import readexcel,add_clientkey_to_headers,base_api
from config import *
import requests


@ddt.ddt
class GetRentHouseList_AreaQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        cls.header=add_clientkey_to_headers.get_clientkey()

    testdata = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求租-面积查询").dict_data()
    @ddt.data(*testdata)
    def test_getRentHouseList_AreaQuery(self, case):
        case["headers"] = self.header
        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)   # json字符串转为字典
        print("检查点->：%s" % check)

        #将检查点的数据组装成一个列表
        lst_check=[]
        high_data=check.get("houseAreaHigh")
        lst_check.append(high_data)
        low_data=check.get("houseAreaLow")
        lst_check.append(low_data)

        # 返回结果
        res_text = res["text"]             # 获取响应的内容
        res_text = json.loads(res_text)    # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)
        rent_list = res_text["data"]["rentCustomers"]
        if len(rent_list) > 0:
            #将一定区间面积的求租客源的数据获取出来
            lst = []
            for i in rent_list:
                rent_area_high = i["houseAreaHigh"]
                lst.append(rent_area_high)
                rent_area_low=i["houseAreaLow"]
                lst.append(rent_area_low)

            #断言
            self.assertIn(lst_check[0], lst)
            self.assertIn(lst_check[1], lst)
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"),res_text["errCode"])
            print("不存在此区间面积的求租客源")


if __name__ == '__main__':
    unittest.main()