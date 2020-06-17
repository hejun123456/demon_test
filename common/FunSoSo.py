

import requests,json
from common import readexcel
from config import *
from common import add_clientkey_to_headers


class FunSoSo():
    #获取搜搜中出售房源，并返回id
    def get_SoSo_houseSale(self):
        headers=add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/sosoWeb/soso/house/getSoSoSaleList"
        data=readexcel.ExcelUtil(SOSO_EXCEL_PATH,sheetName="搜搜-出售信息").dict_data()
        data=json.loads(data[0]["body"])

        res=requests.post(url=url,headers=headers,json=data)
        print(res.json()["data"][0]["id"])
        return str(res.json()["data"][0]["id"]),headers

    #获取搜搜中出售房源电话
    def get_SoSo_houseSalePhone(self):
        self.id,self.headers=self.get_SoSo_houseSale()
        url="http://hft.myfun7.com/erpWeb/soso/house/getSOSOConvertDetectData"
        data = readexcel.ExcelUtil(SOSO_EXCEL_PATH, sheetName="搜搜-查看电话").dict_data()
        dict_data = json.loads(data[0]["body"])
        dict_data.update({"sosoId":self.id})

        res = requests.post(url=url, headers=self.headers, json=dict_data)
        print(res.json()["data"][0]["phone"])
        return str(res.json()["data"][0]["phone"]),self.id,self.headers

    #搜搜中获取的出售房源转入系统之后的信息
    def get_sosoSale_infoById(self):
        url="http://hft.myfun7.com/erpWeb/soso/house/getSaleInDataInfoById"
        self.phone,self.id,self.headers=self.get_SoSo_houseSalePhone()
        data={"sosoId":self.id,"time":"2020-04-23 12:00:26"}

        res = requests.post(url=url, headers=self.headers, json=data)
        print(res.json()["data"])
        return res.json()["data"],self.id

#
# a=FunSoSo()
# id,header=a.get_SoSo_houseSale()
# phone,ids,headers=a.get_SoSo_houseSalePhone()
# print(phone)
# data,data_id=a.get_sosoSale_infoById()
# print(data)

# print(b)
# a.delete_houseSale("12212125465werfr")
# a,b,c,d=a.get_builId("英郡")
# print(a,b,c,d)
#
# a.get_caseId_Sale()




