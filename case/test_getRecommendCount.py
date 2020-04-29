# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,HouseManage,CustomerManage
from common import readexcel
from config import *
from common import add_clientkey_to_headers




#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="获取经纪人下推荐房客源数").dict_data()
print(testdata)

@ddt.ddt
class TestHouseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持会话
        cls.s = requests.session()
        #创建推荐房客源
        cls.caseid_sale=HouseManage.HouseManage().add_recommend_houseSale()
        cls.caseid_lease=HouseManage.HouseManage().add_recommend_houseLease()

        cls.caseid_buy=CustomerManage.CustomerManage().add_recommend_buyCustomer()
        cls.caseid_rent=CustomerManage.CustomerManage().add_recommend_rentCustomer()

        header=add_clientkey_to_headers.get_clientkey()
        cls.header = header
    @classmethod
    def tearDownClass(cls):
        sale_code=HouseManage.HouseManage().delete_houseSale(cls.caseid_sale)
        lease_code=HouseManage.HouseManage().delete_leaseHouse(cls.caseid_lease)
        buy_code=CustomerManage.CustomerManage().delete_buyCustomer(cls.caseid_buy)
        rent_code=CustomerManage.CustomerManage().delete_rentCustomer(cls.caseid_rent)
        if sale_code==200 and lease_code==200 and buy_code==200 and rent_code==200:
            print("推荐房客源删除成功")
        else:
            print("推荐房客源删除失败")

    @ddt.data(*testdata)
    def test_get_recommendCount(self, case):
        case["headers"]=self.header

        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]  #获取检查点中的内容
        check=json.loads(check)         #字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)

        # 断言
        if "errMsg" not in res_text.keys():
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("recommend"),res_text["data"]["recommend"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

# if __name__ == "__main__":
#      unittest.main()
