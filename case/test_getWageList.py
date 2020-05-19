


import unittest,ddt
import requests,json
from common import readexcel,base_api,get_date
from config import *
from common import add_clientkey_to_headers

# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(WAGE_MANAGE_EXCEL_PATH, sheetName="薪资管理-筛选员工薪资列表").dict_data()
print(testdata)

@ddt.ddt
class TestGetWageList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 登录获取clientkey
        cls.s = requests.session()
        header = add_clientkey_to_headers.get_clientkey()
        cls.header = header
    @ddt.data(*testdata)
    def test_getWageList(self,case):
        case["headers"] = self.header
        dic_body=json.loads(case["body"])
        local_month = get_date.GetDate().get_local_month()+","+get_date.GetDate().get_local_month()
        dic_body["assessmentMonth"] = local_month
        str_body = json.dumps(dic_body)
        case.update({"body":str_body})
        print(case)
        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # 字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)


        # 断言
        self.assertEqual(check.get("userName"), res_text["data"][0]["userName"])

if __name__ == "__main__":
     unittest.main()