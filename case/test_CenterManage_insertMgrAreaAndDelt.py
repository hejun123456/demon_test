
# coding:utf-8
# 作者：hejun


import unittest
import ddt
import requests,json
from common import base_api,OrganizationManage
from common import readexcel
from config import *
from common import add_clientkey_to_headers


#读取出excel中的测试数据
testdata = readexcel.ExcelUtil(ORGANIZATION_MANAGE_EXCEL_PATH,sheetName="组织管理-员工档案-增加大区").dict_data()
print(testdata)

@ddt.ddt
class InsertMgrArea(unittest.TestCase):

    def setUp(self):
        # 保持登录状态
        self.s = requests.session()
        self.header=add_clientkey_to_headers.get_clientkey()

    @ddt.data(*testdata)
    def test_insert_mgrArea(self, case):
        case["headers"]=self.header

        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]      #获取检查点中的内容
        check=json.loads(check)         #json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)
        self.res_text=res_text

        if "data" in res_text.keys():
            datas = res_text["data"]
            self.datas = datas

            # 断言
            if "areaId" in datas.keys():
                self.assertIn(check.get("areaId"), datas.keys())
                self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])

    def tearDown(self):
        # 删除增加的大区
        if "data" in self.res_text.keys():
            datas = self.datas
            if "areaId" in datas.keys():
                self.areaid=self.datas["areaId"]
                errCode = OrganizationManage.OrganizationManage().delete_insert_mgr_area(self.areaid)
                if errCode == 200:
                    print("成功删除增加的大区")
        else:
            print("增加大区失败")


if __name__ == "__main__":
     unittest.main()