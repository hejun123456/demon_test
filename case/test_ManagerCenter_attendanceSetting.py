
# coding:utf-8
# 作者：hejun


import unittest,ddt
import requests,json
from common import base_api
from common import readexcel
from config import *
from common import add_clientkey_to_headers


# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(ATTENDANCE_MANAGE_EXCEL_PATH,sheetName="考勤管理-考勤配置-考勤参数").dict_data()
print(testdata)

@ddt.ddt
class TestAttendanceSetting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 登录获取clientkey
        cls.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        # print(header)
        cls.header = header
    @classmethod
    def tearDownClass(cls):
        url="http://hft.myfun7.com/erpWeb/managerCenter/attendanceSettingModule/saveSetting"
        header=cls.header
        data={"id":"43578", "ruleValue":"13"}
        r=requests.post(url,headers=header,json=data)
        if r.json()["data"] == 1:
            print("成功恢复默认的时间")
        else:
            print("恢复默认时间失败")

    @ddt.data(*testdata)
    def test_attendanceSetting(self, case):
        case["headers"]=self.header

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
        if "data" in res_text.keys():
            self.assertEqual(check.get("data"), res_text["data"])
            self.assertEqual(check.get("errCode"), res_text["errCode"])
        else:
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])
            self.assertEqual(check.get("errCode"), res_text["errCode"])

if __name__ == "__main__":
     unittest.main()
