

import unittest,json,ddt
from common import readexcel,add_clientkey_to_headers,base_api
from config import *
import requests


@ddt.ddt
class GetSaleHouseList_PriceQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()

    testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出售-总价格查询").dict_data()
    @ddt.data(*testdata)
    def test_getSaleHouseList_PriceQuery(self, case):
        case["headers"] = add_clientkey_to_headers.get_clientkey()
        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)   # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]             # 获取响应的内容
        res_text = json.loads(res_text)    # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)
        sale_list = res_text["data"]["saleList"]
        if len(sale_list) > 0:
            #将一定区间总价格的出售房源的数据获取出来
            lst = []
            for i in sale_list:
                sale_price = i["saleTotalPrice"]
                lst.append(sale_price)
            lst.sort()      #将出售房源总价格从小到大排序
            #断言
            self.assertGreaterEqual(check.get("saleTotalPrice"), lst[-1])     #a>=b
            self.assertLessEqual(check.get("saleLowPrice"), lst[0])          #a<=b
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            print("不存在此区间总价格的出售房源")


if __name__ == '__main__':
    unittest.main()
