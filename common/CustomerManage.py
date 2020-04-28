


import requests,json
from common import readexcel
from config import *
from common import add_clientkey_to_headers


class CustomerManage():
    #登记求购客源,并返回caseid和headers
    def create_BuyCustomer(self):
        headers=add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/houseWeb/erp/buyCust/createBuyCustomer"
        data=readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH,sheetName="客源管理-求购-登记").dict_data()
        data=json.loads(data[0]["body"])

        res=requests.post(url=url,headers=headers,json=data)
        print(res.json())
        print(res.json()["data"]["caseId"])
        print(headers)
        return res.json()["data"]["caseId"],headers

    #删除求购的客源
    def delete_buyCustomer(self,caseid):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "3",     # 3 代表求购客源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "30"    # 30 代表删除房源
        }
        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]

    # 登记求租客源，并返回caseidhe headers
    def create_RentCustomer(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/erp/rentCust/createRentCustomer"
        data = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求租-登记").dict_data()
        data = json.loads(data[0]["body"])

        res = requests.post(url=url, headers=headers, json=data)
        print(res.json())
        print(res.json()["data"]["caseId"])
        print(headers)
        return res.json()["data"]["caseId"], headers

    #删除求租客源
    def delete_rentCustomer(self,caseid):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data = {
            "caseId": caseid,
            "caseType": "4",  # 4 代表求租客源
            "isSaleLease": "0",  # 是否是租售房源，1=是，0=否  默认是0
            "trackContent": "content",
            "trackType": "30"  # 30 代表删除房源
        }
        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]

    #获取出售中未使用的合同编号
    def get_buyMatchNotAllocatedDealCode(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/erpWeb/managerCenter/transaction/deal/getMatchNotAllocatedDealCodeList"
        data={"dealType":"101"}
        res=requests.post(url,json=data,headers=headers)
        res_dict=res.json()
        return (res_dict["data"]["list"])[0]["codeNo"],headers

    # 获取求租中未使用的合同编号
    def get_rentMatchNotAllocatedDealCode(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/erpWeb/managerCenter/transaction/deal/getMatchNotAllocatedDealCodeList"
        data = {"dealType": "102"}
        res = requests.post(url, json=data, headers=headers)
        res_dict = res.json()
        return (res_dict["data"]["list"])[0]["codeNo"],headers







