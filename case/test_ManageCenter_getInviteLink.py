# coding:utf-8
# 作者：hejun


import unittest, ddt
import requests, json
from common import base_api
from common import readexcel,add_clientkey_to_headers,untils
from config import *

# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(ORGANIZATION_MANAGE_EXCEL_PATH, sheetName="获取新建员工邀请链接").dict_data()
print(testdata)


@ddt.ddt
class GetInviteLink(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        cls.header= add_clientkey_to_headers.get_clientkey()

    @ddt.data(*testdata)
    def test_get_invite_link(self, case):
        dic_data = json.loads(case["body"])
        if dic_data["CLIENTKEY"]=="":
            case["headers"] = self.header
        else:
            case["headers"] = self.header
            dic_data["CLIENTKEY"] = self.header["CLIENTKEY"]
            str_data=json.dumps(dic_data)
            case.update({"body":str_data})

        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)
        self.res_text = res_text

        # 断言
        self.assertEqual(check.get("errCode"), res_text["errCode"])


if __name__ == "__main__":
    unittest.main()
