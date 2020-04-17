

import requests,json
from common import base_api
from common import readexcel
from config import *
from common import add_clientkey_to_headers


class HouseMansge():
    #登记出售房源
    def create_houseSale(self):
        headers=add_clientkey_to_headers.get_clientkey()
        url="http://hft.myfun7.com/houseWeb/funSale/createFunSale"
        data={"buildCode":"BGY",
                   "buildId":"2051071",
                   "buildName":"碧桂园",
                   "checkCodeFun":"",
                   "effectiveDate":"",
                   "guarantyType":"",
                   "houseSituation":"",
                   "houseSituationId":"",
                   "houseSituationText":"请选择",
                   "onlyTextCore":"好",
                   "onlyTextFitment":"好",
                   "onlyTextLayout":"好",
                   "onlyTextRights":"无",
                   "ownershipType":"",
                   "ownershipTypeId":"",
                   "ownershipTypeText":"请选择",
                   "phones":[{"idCard":"",
                              "idCardType":"1",
                              "ownerName":"何",
                              "ownerSex":"1",
                              "ownerType":"0",
                              "phone":"13684089105",
                              "phoneType":"1",
                              "seqNo":"1"},
                             {"phone":"",
                              "phoneType":"",
                              "seqNo":"2"},
                             {"idCard":"",
                              "idCardType":"1",
                              "ownerName":"",
                              "ownerSex":"1","ownerType":"1","phone":"","phoneType":"","seqNo":"3"},{"idCard":"","idCardType":"1","ownerName":"","ownerSex":"1","ownerType":"1","phone":"","phoneType":"","seqNo":"4"}],"plateType":"2","qzCodeFun":"","receiptType":"","regionName":"高新区","repeatFlag":"1","saleArea":"50","saleBuyPrice":"","saleDirect":"","saleDirectText":"请选择","saleDoors":"6","saleFitment":"3","saleFitmentText":"精装","saleFloor":"8","saleFloors":"30","saleGradation":"1","saleHall":"10","saleId":"","saleInnerarea":"","saleLadder":"8","saleLeaveTime":"","saleLevel":"1","saleLowestPrice":"50","saleMemo":"","saleNature":"1","saleNo":"","saleNum":"8","saleNumR":"8","saleReg":"4","saleRight":"1","saleRoof":"8","saleRoofR":"8","saleRoom":"10","saleRound":"6","saleRoundText":"郊县","saleSource":"1","saleStorey":"","saleStreet":"0","saleStruct":"","saleStructId":"","saleStructText":"请选择","saleSubject":"很好的非二而服务费个人俄","saleTotalPrice":"50","saleType":"1","saleUnit":"8","saleUnitPrice":"10000","saleUnitR":"8","saleUseage":"1","saleWei":"10","saleYang":"10","saleYear":"2019","sectionId":"","sectionName":"南延线","showPhone":"1","tagIds":"","tradeAddr":"","unitFloor":"8","unitFloorR":"8"}

        res=requests.post(url=url,headers=headers,json=data)
        return res.json()["data"]["caseId"],res.headers
        # print(res.json()["data"]["caseId"])



    #获取出售中的房源id
    def get_caseId_Sale(self):
        caseId,headers=self.create_houseSale()
        print(caseId)
        return caseId

    #删除出售中的房源
    def delete_houseSale(self,content):
        caseid,headers=self.create_houseSale()   #获取登记后房源的id和headers信息

        #删除登记的房源
        url="http://hft.myfun7.com/houseWeb/houseCust/createTrackInfo"
        data={"caseId":caseid,
              "caseType":"1",
              "isSaleLease":"0",
              "trackContent":content,
              "trackType":"30"
              }

        res=requests.post(url=url,json=data,headers=headers)
        print(res.text)
        print(res.json()["errCode"])

a=HouseMansge()
a.delete_houseSale()
# a.create_houseSale()
# a.get_caseId_Sale()




