
# coding:utf-8
# 作者：hejun


import unittest,ddt
import requests,json
from common import base_api,AttendanceManage,get_date
from common import readexcel
from config import *



# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(ATTENDANCE_MANAGE_EXCEL_PATH,sheetName="考勤管理-新增考勤组").dict_data()
print(testdata)

@ddt.ddt
class TestAddAttendanceGroup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        # 创建考勤班次
        cls.data_id, cls.header=AttendanceManage.AttendanceManage().create_attendance_class()

    def tearDown(self):
        # 将考勤组里面的人员设置为空
        if "data" in self.res_text.keys():
            url = "http://hft.myfun7.com/erpWeb/managerCenter/attendanceGroupModule/addEditAttendanceGroup"
            data = {"attendanceScheduleList":"[]",
                    "classType":"2","groupBizList":"[]",
                    "groupName":"自动化考勤组",
                    "id":self.res_text["data"],
                    "isUpdateUser":"1",
                    "needDelUserIds":"20174961"
                    }
            r = requests.post(url, headers=self.header, json=data)
            print(r.json())
            if r.json()["data"] == self.res_text["data"]:
                print("成功清空考勤组里面的人员")
            else:
                print("清空考勤组人员失败")

            # 删除考勤组
            data_code=AttendanceManage.AttendanceManage().delete_attendance_group(self.header,self.res_text["data"])
            if data_code == 1:
                print("考勤组已删除")
            else:
                print("考勤组删除失败")

            # 删除考勤班次
            code=AttendanceManage.AttendanceManage().delete_attendance_class(self.header,self.data_id)
            if code == 1:
                print("考勤班次已删除")
            else:
                print("考勤班次删除失败")
        else:
            print("考勤组创建失败")

    @ddt.data(*testdata)
    def test_add_attendance_group(self, case):
        case["headers"] = self.header
        body_dic_data=json.loads(case["body"])
        str_data = body_dic_data["attendanceScheduleList"]
        dic_data = (json.loads(str_data))[0]     #将字符串转化为字典，并组装成了列表后取第一个元素

        dic_data["attClassId"]=str(self.data_id)
        dic_data["attTime"]=get_date.GetDate().get_tomorrow_data_time_hourse()
        lst=[]    # 创建一个空列表，用于存放字典
        lst.append(dic_data)
        b=json.dumps(lst)
        body_dic_data.update({"attendanceScheduleList":b})

        a=json.dumps(body_dic_data)
        case.update({"body": a})

        res = base_api.send_requests(self.s,case)

        # 检查点 checkpoint
        check = case["checkpoint"]      #获取检查点中的内容
        check=json.loads(check)         #字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)
        self.res_text = res_text
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
