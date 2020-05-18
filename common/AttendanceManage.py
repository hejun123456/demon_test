import requests,json
from common import readexcel
from config import *
from common import add_clientkey_to_headers

class AttendanceManage():
    # 创建考勤地点
    def create_attendance_scope(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/erpWeb/managerCenter/attendanceScopeModule/addEditAttendanceScope"
        data = readexcel.ExcelUtil(ATTENDANCE_MANAGE_EXCEL_PATH, sheetName="考勤管理-考勤配置-新增考勤地点").dict_data()
        data = json.loads(data[0]["body"])

        res = requests.post(url=url, headers=headers, json=data)
        print(res.json()["data"])
        return res.json()["data"], headers

    # 删除考勤地点
    def delete_attendance_scope(self,header,attendance_id):
        url="http://hft.myfun7.com/erpWeb/managerCenter/attendanceScopeModule/delAttendanceScope"
        data={"attScopeId": attendance_id}
        res = requests.post(url=url, headers=header, json=data)
        print(res.json()["data"])
        return res.json()["data"]

    # 增加考勤班次
    def create_attendance_class(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/erpWeb/managerCenter/attendanceClassModule/addEditAttendanceClass"
        data = readexcel.ExcelUtil(ATTENDANCE_MANAGE_EXCEL_PATH, sheetName="考勤管理-新增考勤班次").dict_data()
        data = json.loads(data[0]["body"])

        res = requests.post(url=url, headers=headers, json=data)
        print(res.json()["data"])
        return res.json()["data"], headers

    # 删除考勤班次
    def delete_attendance_class(self,header,class_id):
        url = "http://hft.myfun7.com/erpWeb/managerCenter/attendanceClassModule/delAttendanceClass"
        data = {"id": class_id}
        res = requests.post(url=url, headers=header, json=data)
        print(res.json()["data"])
        return res.json()["data"]
    # 删除考勤组
    def delete_attendance_group(self,header,group_id):
        url = "http://hft.myfun7.com/erpWeb/managerCenter/attendanceGroupModule/delAttendanceGroup"
        data = {"id": group_id}
        res = requests.post(url=url, headers=header, json=data)
        print(res.json()["data"])
        return res.json()["data"]