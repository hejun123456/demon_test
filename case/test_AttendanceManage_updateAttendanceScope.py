
# coding:utf-8
# 作者：hejun


import unittest,ddt
import requests,json
from common import base_api,AttendanceManage
from common import readexcel
from config import *



# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(ATTENDANCE_MANAGE_EXCEL_PATH, sheetName="考勤管理-考勤配置-更新考勤地点").dict_data()
print(testdata)

@ddt.ddt
class TestUpdateAttendanceScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 登录获取clientkey
        cls.s = requests.session()
        # 创建考勤地点
        cls.attendance_id, cls.header = AttendanceManage.AttendanceManage().create_attendance_scope()

    def tearDown(self):
        # 将考勤地点里面的人员设置为空
        if "data" in self.res_text.keys():
            url="http://hft.myfun7.com/erpWeb/managerCenter/attendanceScopeModule/addEditAttendanceScope"
            header=self.header
            data={"attDistance":"100","attScopeId":self.attendance_id,
                  "attScopeX":"104.063089","attScopeY":"30.571901",
                  "attdanceScopeBizList":"[]","isUpdateUser":"1",
                  "locationDesc":"四川省成都市武侯区桂溪街道天府大道北段1647号","locationDescAbb":"成都市纪委"
                  }
            r=requests.post(url,headers=header,json=data)
            if r.json()["data"] == self.attendance_id:
                print("成功清空考勤人员")
            else:
                print("清空考勤人员失败")
    @classmethod
    def tearDownClass(cls):
        # 删除增加的考勤地点
        code=AttendanceManage.AttendanceManage().delete_attendance_scope(cls.header,cls.attendance_id)
        # url = "http://hft.myfun7.com/erpWeb/managerCenter/attendanceScopeModule/delAttendanceScope"
        # header = cls.header
        # data = {"attScopeId": cls.attendance_id}
        # r = requests.post(url, headers=header, json=data)
        if code == 1:
            print("成功删除考勤地点")
        else:
            print("删除考勤地点失败")


    @ddt.data(*testdata)
    def test_update_attendance_scope(self, case):
        case["headers"]=self.header
        body_data=json.loads(case["body"])
        body_data["attScopeId"]=self.attendance_id
        body_str_data=json.dumps(body_data)
        case.update({"body":body_str_data})

        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  #获取检查点中的内容
        check=json.loads(check)         #字符串转为字典
        print("检查点->：%s" % check)


        # 返回结果
        res_text = res["text"]          #获取响应的内容
        res_text=json.loads(res_text)   #将响应的内容转换为字典
        print("返回实际结果->：%s"%res_text)
        self.res_text=res_text

        if "data" in check.keys():
            check["data"]=res_text["data"]    # 将返回的data写入到检测点中去，方便后面的断言
            # 断言
            if "data" in res_text.keys():
                self.assertEqual(check.get("data"), res_text["data"])
                self.assertEqual(check.get("errCode"), res_text["errCode"])

        else:
            self.assertEqual(check.get("errCode"), res_text["errCode"])


if __name__ == "__main__":
     unittest.main()
