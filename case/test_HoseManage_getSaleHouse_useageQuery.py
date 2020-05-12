

import unittest,json,ddt
from common import readexcel,add_clientkey_to_headers,base_api,Logout_Systerm
from config import *
import requests


@ddt.ddt
class GetSaleHouseList_useageQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态并获取到clientkey值
        cls.s = requests.session()
        cls.header=add_clientkey_to_headers.get_clientkey()

    @classmethod
    def tearDownClass(cls):
        clientkey=cls.header["CLIENTKEY"]
        Logout_Systerm.Logout(clientkey)

    testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出售-房源用途查询").dict_data()
    @ddt.data(*testdata)
    def test_getSaleHouseList_useageQuery(self, case):
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
        sale_list = res_text["data"]["saleList"]
        if len(sale_list) > 0:
            #将返回值中用途值获取出来
            lst = []
            for i in sale_list:
                sale_useage = i["saleUseage"]
                lst.append(sale_useage)
            lst_data=list(set(lst))
            if len(lst_data) == 1:
                #断言
                self.assertEqual(check.get("saleUseage"), lst[0])
                self.assertEqual(check.get("errCode"), res_text["errCode"])
            else:
                print("搜索出房源的用途不全为对应房源")
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            print("不存在对应用途的房源")


if __name__ == '__main__':
    unittest.main()