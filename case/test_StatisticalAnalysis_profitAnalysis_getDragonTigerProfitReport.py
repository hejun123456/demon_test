# coding:utf-8
# 作者：hejun


import unittest,ddt
import requests,json
from common import base_api,get_date
from common import readexcel
from config import *
from common import add_clientkey_to_headers




# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(STATISTICAL_ANALYSIS_EXCEL_PATH,sheetName="统计分析-业绩排行榜").dict_data()
print(testdata)

@ddt.ddt
class TestStatisticalAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 登录获取clientkey
        cls.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        # print(header)
        cls.header = header

    @ddt.data(*testdata)
    def test_getDragonTigerProfitReport(self, case):
        case["headers"]=self.header
        a = json.loads(case["body"])
        a["endTime"] =get_date.GetDate().get_local_month()
        a["startTime"]=get_date.GetDate().get_local_month()
        b = json.dumps(a)
        case.update({"body": b})

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
        self.assertIn(check.get("dimension"),res_text["data"].values())
        self.assertEqual(check.get("errCode"),res_text["errCode"])

if __name__ == "__main__":
     unittest.main()
