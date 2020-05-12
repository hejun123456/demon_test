

import requests,json,ddt,unittest
from common import readexcel,base_api,HouseManage
from config import *
from time import sleep

@ddt.ddt
class SaleHouseUnitPriceOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        #创建出售中按照单价来排序的房源
        cls.Lower_caseid=HouseManage.SaleHouseOrder().create_SaleHouse_unitPriceLow()
        cls.High_caseid,cls.headers=HouseManage.SaleHouseOrder().create_SaleHouse_unitPriceHigh()
        sleep(10)

    @classmethod
    def tearDownClass(cls):
        lower_coed=HouseManage.HouseManage().delete_houseSale(cls.Lower_caseid)
        high_code=HouseManage.HouseManage().delete_houseSale(cls.High_caseid)

        if lower_coed == 200 and high_code == 200:
            print("房源删除成功")
        else:
            print("房源删除失败")


    #出售房源按照单价排序
    data = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出售-单价排序").dict_data()
    print(data)
    @ddt.data(*data)
    def test_saleHouse_unit_PriceOrder(self,case):
        case["headers"] = self.headers
        res = base_api.send_requests(self.s, case)
        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)   # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        # 断言
        self.assertEqual(check.get("saleUnitPrice"), res_text["data"]["saleList"][0]["saleUnitPrice"])
        self.assertEqual(check.get("buildName"), res_text["data"]["saleList"][0]["buildName"])
        self.assertEqual(check.get("errCode"), res_text["errCode"])



if __name__ == '__main__':
        unittest.main()
