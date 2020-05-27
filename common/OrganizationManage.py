

import requests,json
from common import readexcel,untils
from config import *
from common import add_clientkey_to_headers

class OrganizationManage():
    #增加大区，返回大区id
    def insert_mgr_area(self):
        headers=add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/erpWeb/managerCenter/organization/insertMgrArea"
        data=readexcel.ExcelUtil(ORGANIZATION_MANAGE_EXCEL_PATH,sheetName="组织管理-员工档案-增加大区").dict_data()
        data=json.loads(data[0]["body"])

        res=requests.post(url=url,headers=headers,json=data)
        print(res.json()["data"]["areaId"])
        return res.json()["data"]["areaId"],headers

    # 删除增加的大区方法
    def delete_insert_mgr_area(self,areaId):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/erpWeb/managerCenter/organization/deleteMgrArea"
        data = {"areaId": areaId}
        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]

    # 增加片区
    def insert_mgr_range(self,header):
        url = "http://hft.myfun7.com/erpWeb/managerCenter/organization/insertMgrRangeData"
        data = readexcel.ExcelUtil(ORGANIZATION_MANAGE_EXCEL_PATH, sheetName="组织管理-员工档案-增加片区").dict_data()
        data = json.loads(data[0]["body"])

        res = requests.post(url=url, headers=header, json=data)
        return res.json()["data"]["regId"]


    #删除增加的片区
    def delete_insert_mgr_range(self, regid, header):
        url = "http://hft.myfun7.com/erpWeb/managerCenter/organization/deleteMgrRangeData"
        data = {"regId": regid}
        headers=header
        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]

    # 提交员工邀请信息
    def add_InviteUserInfo(self):
        self.header=add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/erpWeb/managerCenter/organization/addInviteUserInfo"
        data = readexcel.ExcelUtil(ORGANIZATION_MANAGE_EXCEL_PATH, sheetName="邀请注册接口").dict_data()[0]
        dic_data=json.loads(data["body"])
        dic_data["userMobile"]=untils.CreatePhone().create_phone()
        str_data=json.dumps(dic_data)
        data.update({"body":str_data})

        r=requests.post(url,headers=self.header,json=json.loads(data["body"]))
        return (dic_data["serviceReg"], dic_data["serviceZoneIds"], dic_data["serviceZone"],
                dic_data["userMobile"], self.header, dic_data["userName"])

    # 获取邀请的链接参数
    def get_inviteLink(self,a):
        url="http://hft.myfun7.com/erpWeb/managerCenter/organization/getInviteLink"
        data={}
        datas=a["CLIENTKEY"]
        data.update({"CLIENTKEY":datas})
        res=requests.post(url=url, headers=a, json=data)
        link_params = res.json()["data"]["inviteLink"].split("?")[1].split("=")[1]
        return link_params

    # 获取邀请id
    def get_inviteUserId(self,link_params,userMobile):
        url = "http://erpweb.myfun7.com/erpWeb/openApi/inviteRegist/validateCompInviteMsg"
        data = {"param": link_params,
                "userMobile": userMobile,
                "code": "859652"}
        r = requests.post(url, data=data)
        return r.json()["data"]["inviteId"]

    # 按关键字查询添加的员工
    def get_UserListInfo(self,key_word,header):
        url="http://hft.myfun7.com/erpWeb/managerCenter/organization/getUserListInfo"
        data={"compId":"57422","deptId":"904205","keyWord":key_word}
        r=requests.post(url,headers=header,json=data)
        return r.json()["data"]
    # 注销员工
    def delete_user(self,userid,header):
        url="http://hft.myfun7.com/erpWeb/managerCenter/organization/deleteUser"
        data={"userId": userid}
        r=requests.post(url,headers=header,json=data)
        return r.json()["errCode"]