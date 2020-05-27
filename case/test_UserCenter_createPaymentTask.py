


import unittest,json,ddt
from common import readexcel,login_get_clientkey
from config import *
import requests

testdata = readexcel.ExcelUtil(USER_MANAGE_EXCEL_PATH,sheetName="创建充值金额接口").dict_data()
print(testdata)

@ddt.ddt
class CreatePaymentTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        cls.clientkey = login_get_clientkey.login()


    @ddt.data(*testdata)
    def test_create_paymentTask(self, case):
        dic_header = json.loads(case["headers"])
        dic_header["CLIENTKEY"] = self.clientkey
        dic_body_data = json.loads(case["body"])
        print(dic_header)
        res = requests.post(url=case["url"],headers=dic_header,data=dic_body_data)


        # 检查点 checkpoint
        check = case["checkpoint"]    # 获取检查点中的值
        check = json.loads(check)     # 将son字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res.json()   # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        #断言
        self.assertIn(check.get("msg"), res_text["msg"])
        self.assertEqual(check.get("errCode"),res_text["errCode"])


if __name__ == '__main__':
    unittest.main()



