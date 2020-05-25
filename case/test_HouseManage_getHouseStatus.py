




import unittest,json
from common.HouseManage import HouseManage,HouseStatus
from common import readexcel,base_api,add_clientkey_to_headers
import requests,ddt
from config import *
from time import sleep


@ddt.ddt
class GetHouseStatus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        #创建5个出售房源
        lst = []
        for i in range(0, 5):
            caseid,headers=HouseManage().create_houseSale()
            a=caseid
            lst.append(a)
            print(lst)
        #分别将创建的5个房源写成封盘、预定、暂缓、内成交以及外成交状态
        cls.caseid_a=HouseStatus().create_fengPan(lst[0])
        cls.caseid_b=HouseStatus().create_yuDing(lst[1])
        cls.caseid_c=HouseStatus().create_zanHuan(lst[2])
        cls.caseid_d=HouseStatus().create_neiChengJiao(lst[3])
        cls.caseid_e=HouseStatus().create_waiChengJiao(lst[4])
        sleep(5)
        return lst

    @classmethod
    def tearDownClass(cls):
        #删除登记的房源
        code_a=HouseManage().delete_houseSale(cls.caseid_a)
        code_b = HouseManage().delete_houseSale(cls.caseid_b)
        code_c = HouseManage().delete_houseSale(cls.caseid_c)
        code_d = HouseManage().delete_houseSale(cls.caseid_d)
        code_e = HouseManage().delete_houseSale(cls.caseid_e)
        if code_a==200 and code_b==200 and code_c==200 and code_d==200 and code_e==200:
            print("房源删除成功")
        else:
            print("房源删除失败")

    testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出售-房源状态").dict_data()
    print(testdata)
    @ddt.data(*testdata)
    def test_get_HouseStatus(self, case):
        case["headers"] = add_clientkey_to_headers.get_clientkey()
        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)   # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]   # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        # 断言
        self.assertEqual(check.get("userName"), res_text["data"]["saleList"][0]["userName"])
        self.assertEqual(check.get("saleSubject"), res_text["data"]["saleList"][0]["saleSubject"])


if __name__ == '__main__':
        unittest.main()
