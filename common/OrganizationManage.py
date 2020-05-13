import requests,json
from common import readexcel,get_date
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

