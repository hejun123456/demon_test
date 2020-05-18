# coding:utf-8
# 作者：hejun


import unittest,ddt
import requests,json
from common import base_api,AttendanceManage
from common import readexcel
from config import *
from common import add_clientkey_to_headers


# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(ATTENDANCE_MANAGE_EXCEL_PATH,sheetName="考勤管理-新增考勤班次").dict_data()
print(testdata)

@ddt.ddt
class TestAddAttendanceClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 登录获取clientkey
        cls.s = requests.session()
        header=add_clientkey_to_headers.get_clientkey()
        cls.header = header

    def tearDown(self):
        # 删除考勤班次
        if "data" in self.res_text.keys():
            id = self.res_text["data"]
            code=AttendanceManage.AttendanceManage().delete_attendance_class(self.header, id)
            if code == 1:
                print("考勤班次删除成功")
            else:
                print("考勤班次删除失败")
        else:
            print("不存在要删除的考勤班次")


    @ddt.data(*testdata)
    def test_add_attendance_class(self, case):
        case["headers"]=self.header

        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]      #获取检查点中的内容
        check=json.loads(check)         #字符串转为字典
        print("检查点->：%s" % check)


        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)
        self.res_text=res_text

        if "data" in check.keys():
            check["data"]=res_text["data"]    # 将返回的data写入到检测点中去，方便后面的断言
            self.data = check["data"]
            # 断言
            if "data" in res_text.keys():
                self.assertEqual(check.get("data"), res_text["data"])
                self.assertEqual(check.get("errCode"), res_text["errCode"])

        else:
            self.assertEqual(check.get("errMsg"), res_text["errMsg"])
            self.assertEqual(check.get("errCode"), res_text["errCode"])

if __name__ == "__main__":
     unittest.main()