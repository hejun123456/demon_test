

import unittest,json,ddt
from common import readexcel,add_clientkey_to_headers,base_api,HouseManage
from config import *
import requests


@ddt.ddt
class GetSaleHouseList_BuildNameQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        cls.build_id=HouseManage.GetHouseFloorMenu().get_houseFloorMenu()

    testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出售-楼盘名查询").dict_data()
    @ddt.data(*testdata)
    def test_getSaleHouseList_BuildNameQuery(self, case):
        case["headers"] = add_clientkey_to_headers.get_clientkey()
        a=json.loads(case["body"])
        a["buildId"]=self.build_id
        b=json.dumps(a)
        case.update({"body":b})
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
            #将楼盘名获取出来
            lst = []
            for i in sale_list:
                build_name=i["buildName"]
                lst.append(build_name)
            print(lst)
            lst_set = list(set(lst))
            print(lst_set)
            if len(lst_set) == 1:
                self.assertEqual(check.get("buildName"), lst_set[0])
            else:
                print("楼盘名不一致")
        else:
            print("不存在楼盘名为：%s" %(check.get("buildName")))

if __name__ == '__main__':
    unittest.main()

