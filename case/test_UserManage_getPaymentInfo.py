


import unittest,json,ddt
from common import readexcel,untils
from config import *
import requests
from bs4 import BeautifulSoup


testdata = readexcel.ExcelUtil(USER_MANAGE_EXCEL_PATH,sheetName="获取充值页面").dict_data()
print(testdata)

@ddt.ddt
class GetPaymentInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @ddt.data(*testdata)
    def test_get_paymentInfo(self, case):
        money_data=json.loads(case["params"])
        money_datas=money_data["totalMoney"]
        pay_id, token = untils.Payment().create_paymentTask(money_datas)
        print(pay_id,token)
        data={"ptId":pay_id,
              "token":token}
        res = requests.get(url=case["url"],params=data)

        # 检查点 checkpoint
        check = case["checkpoint"]    # 获取检查点中的内容
        check = json.loads(check)     # json字符串转为字典
        print("检查点->：%s" % check)
        check["交易金额"] = money_datas

        # 获取html中相关内容
        html = res.content.decode("UTF-8")
        bs_xml=BeautifulSoup(html)
        bs_xml.prettify()
        div=bs_xml.find("div", {"class": "dd_info"})
        html_text=div.get_text()
        print(html_text)

        # 断言
        self.assertIn(check.get("交易金额"), html_text)


if __name__ == '__main__':
    unittest.main()



