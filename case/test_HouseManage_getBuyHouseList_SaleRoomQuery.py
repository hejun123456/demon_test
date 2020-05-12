

import unittest,json,ddt
from common import readexcel,add_clientkey_to_headers,base_api
from config import *
import requests


@ddt.ddt
class GetBuyHouseList_SaleRoomQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        cls.header=add_clientkey_to_headers.get_clientkey()

    testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出售-户型查询").dict_data()
    @ddt.data(*testdata)
    def test_getBuyHouseList_SaleRoomQuery(self, case):
        case["headers"] = self.header
        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)   # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]             # 获取响应的内容
        res_text = json.loads(res_text)    # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)
        buy_sale_house_datas = res_text["data"]["saleList"]

        #判断传入的户型参数存在一定区间
        if "roomNumHigh" and "roomNumLow" in check.keys():
            if len(buy_sale_house_datas) > 0:
                #将一定户型的出售房源数据获取出来
                lst = []
                for i in buy_sale_house_datas:
                    buy_sale_house_data=i["saleRoom"]
                    lst.append(buy_sale_house_data)

                #断言
                self.assertIn(check.get("roomNumHigh"),lst)
                self.assertIn(check.get("roomNumLow"),lst)
                self.assertEqual(check.get("errCode"), res_text["errCode"])
            else:
                self.assertEqual(check.get("errCode"),res_text["errCode"])
                print("不存在此区间户型的出售户型")
        else:
            if len(buy_sale_house_datas) > 0:
                #将一定户型的出售房源数据获取出来
                lst = []
                for i in buy_sale_house_datas:
                    buy_sale_house_data=i["saleRoom"]
                    lst.append(buy_sale_house_data)

                #断言
                self.assertIn(check.get("saleRoom"),lst)
                self.assertEqual(check.get("errCode"), res_text["errCode"])
            else:

                self.assertEqual(check.get("errCode"), res_text["errCode"])
                print("不存在此区间户型的出售户型")

if __name__ == '__main__':
    unittest.main()

