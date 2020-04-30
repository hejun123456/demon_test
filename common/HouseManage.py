

import requests,json
from common import readexcel
from config import *
from common import add_clientkey_to_headers


class HouseManage():
    #登记出售房源,并返回caseid和headers
    def create_houseSale(self):
        headers=add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/houseWeb/funSale/createFunSale"
        data=readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH,sheetName="房源管理-出售-登记").dict_data()
        data=json.loads(data[0]["body"])

        res=requests.post(url=url,headers=headers,json=data)

        print(res.json()["data"]["caseId"])

        return res.json()["data"]["caseId"],headers

    #出售房源加密跟进日志
    def add_pwd_houseSale(self):
        caseid,headers=self.create_houseSale()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "1",  # 1 代表出售中的房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "17"  #17 代表加密跟进
        }
        requests.post(url=url, json=data, headers=headers)
        return caseid

    # 出售房源推荐跟进日志
    def add_recommend_houseSale(self):
        caseid, headers = self.create_houseSale()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "1",  # 1 代表出售中的房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "18"  # 18 代表推荐跟进
        }
        requests.post(url=url, json=data, headers=headers)
        return caseid

    #删除出售中的房源
    def delete_houseSale(self,caseid):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "1",     # 1 代表出售中的房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "30"    # 30 代表删除房源
        }
        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]

    # 登记出租房源，并返回caseid和headers
    def create_houseLease(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/funLease/createFunLease"
        data = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出租-登记").dict_data()
        data = json.loads(data[0]["body"])

        res = requests.post(url=url, headers=headers, json=data)
        print(res.json()["data"]["caseId"])
        return res.json()["data"]["caseId"], headers

    # 出租房源加密跟进日志
    def add_pwd_houseLease(self):
        caseid, headers = self.create_houseLease()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "2",  # 2 代表出租中的房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "17"  # 17 代表加密跟进
        }
        requests.post(url=url, json=data, headers=headers)
        return caseid

    # 出租房源推荐跟进日志
    def add_recommend_houseLease(self):
        caseid, headers = self.create_houseLease()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "2",  # 1 代表出租中的房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "18"  # 18 代表推荐跟进
        }
        requests.post(url=url, json=data, headers=headers)
        return caseid

    #删除出租房源
    def delete_leaseHouse(self,caseid):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "2",     # 2 代表出租中的房源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "30"  # 30 代表删除房源
        }
        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]

    #获取楼盘信息
    def get_builId(self,para):
        headers = add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/erpWeb/managerCenter/buildRule/getHouseFloorMenu"
        data={"para":para}
        res=requests.post(url,json=data,headers=headers)
        buiddatd=res.json()["data"]["buildInfoVOS"][0]
        return buiddatd["buildId"],buiddatd["buildName"],buiddatd["buildCode"],headers

    #提交出售中房源的钥匙
    def submitKey_houseSale(self,caseid):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/house/submitKey"
        data = {"caseId":caseid,
                "caseType":"1",
                "key":"1","keyDeptId":"904205",
                "keyVoucher":"oss/online/tmp/2020/04/15/646cbc8db6574b1991b7bbbded72c339.jpg",
                "trackContent":"收到钥匙"}

        requests.post(url, json=data, headers=headers)
        return headers










