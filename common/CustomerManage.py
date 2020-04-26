


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

    # 登记求租客源，并返回caseidhe headers
    def create_RentCustomer(self):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/houseWeb/erp/rentCust/createRentCustomer"
        data = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="客源管理-求租-登记").dict_data()
        data = json.loads(data[0]["body"])

        res = requests.post(url=url, headers=headers, json=data)
        print(res.json())
        print(res.json()["data"]["caseId"])
        print(headers)
        return res.json()["data"]["caseId"], headers


# a=HouseMansge()
# a.create_houseSale()
# a.delete_houseSale("12212125465werfr")
# a,b,c,d=a.get_builId("英郡")
# print(a,b,c,d)

# a.get_caseId_Sale()




