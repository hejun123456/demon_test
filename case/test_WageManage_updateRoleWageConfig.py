# coding:utf-8
# 作者：hejun


import unittest,ddt
import requests,json
from common import base_api,WageManage
from common import readexcel
from config import *
from common import add_clientkey_to_headers


# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(WAGE_MANAGE_EXCEL_PATH, sheetName="薪资管理-薪资配置和提成配置").dict_data()
print(testdata)

@ddt.ddt
class TestUpdateRoleWageConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 登录获取clientkey
        cls.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        cls.header = header

    def tearDown(self):
        # 还原薪资配置
        if "wageConfigId" in self.res_text["data"].keys():
            code = WageManage.WageManage().delete_wageRoleConfig(self.header, self.ids)
            if code == 200:
                print("对应角色薪资配置已还原")
            else:
                print("对应角色不存在")
        else:
            print("不存在配置信息")

    @ddt.data(*testdata)
    def test_update_roleWageConfig(self, case):
        case["headers"]=self.header

        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]      #获取检查点中的内容
        check = json.loads(check)         #字符串转为字典
        print("检查点->：%s" % check)


        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)
        self.res_text=res_text
        self.ids=str(res_text["data"]["wageConfigId"])

        if "wageConfigId" in check.keys():
            check["wageConfigId"]=res_text["data"]["wageConfigId"]
            # self.data = check["data"]
            # 断言
            if "wageConfigId" in res_text["data"].keys():
                self.assertEqual(check.get("wageConfigId"), res_text["data"]["wageConfigId"])
                self.assertEqual(check.get("errCode"), res_text["errCode"])

        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])

if __name__ == "__main__":
     unittest.main()