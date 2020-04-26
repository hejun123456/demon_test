

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
        print(res.json())
        print(res.json()["data"]["caseId"])
        print(headers)
        return res.json()["data"]["caseId"],headers

    # 登记出租房源，并返回caseidhe headers
    def create_houseLease(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/funLease/createFunLease"
        data = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="房源管理-出租-登记").dict_data()
        data = json.loads(data[0]["body"])

        res = requests.post(url=url, headers=headers, json=data)
        print(res.json())
        print(res.json()["data"]["caseId"])
        print(headers)
        return res.json()["data"]["caseId"], headers

    # 删除出售中的房源
    def delete_houseSale(self, content):
        # 获取登记后房源的id和headers信息
        caseid, headers = self.create_houseSale()

        # 删除登记的出售房源
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {"caseId": caseid,
                "caseType": "1",
                "isSaleLease": "0",
                "trackContent": content,
                "trackType": "30"
                }
        res = requests.post(url=url, json=data, headers=headers)
        print(res.text)
        print(res.json()["errCode"])
        return res.json()["errCode"]


    #获取楼盘信息
    def get_builId(self,para):
        headers = add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/erpWeb/managerCenter/buildRule/getHouseFloorMenu"
        data={"para":para}
        res=requests.post(url,json=data,headers=headers)
        buiddatd=res.json()["data"]["buildInfoVOS"][0]
        return buiddatd["buildId"],buiddatd["buildName"],buiddatd["buildCode"],headers








# a=HouseMansge()
# a.create_houseSale()
# a.delete_houseSale("12212125465werfr")
# a,b,c,d=a.get_builId("英郡")
# print(a,b,c,d)

# a.get_caseId_Sale()




