



import requests,json
from common import base_api,CustomerManage,HouseManage,get_date
from common import readexcel,add_clientkey_to_headers
from config import *


class TransactionDeal():
    # 创建出售合同
    def create_transaction_deal(self):
        self.s = requests.session()
        # 登记出售房源并获取房源id
        self.sale_caseid, self.sale_no = HouseManage.HouseManage().get_saleHouse_caseNo()
        # 登记求购客源并获取id
        self.caseid, self.header = CustomerManage.CustomerManage().create_BuyCustomer()
        # 获取出售中未使用的合同编号
        self.codeNo, self.headers = CustomerManage.CustomerManage().get_buyMatchNotAllocatedDealCode()
        # 读取出excel中的测试数据
        case = readexcel.ExcelUtil(CUSTOMER_MANAGE_EXCEL_PATH, sheetName="客源管理-求购-新增合同").dict_data()[1]
        print(case)
        a = json.loads(case["body"])
        case["headers"] = self.headers
        a["custId"] = self.caseid
        a["dealCustomerId"] = self.caseid
        a["signDate"] = get_date.GetDate().get_today_str_data()
        a["contractNo"] = self.codeNo
        a["dealHouseId"] = self.sale_caseid
        a["dealHouseNo"] = self.sale_no
        b = json.dumps(a)
        case.update({"body": b})
        res = base_api.send_requests(self.s, case)
        res_text=json.loads(res["text"])
        return res_text["data"]["dealId"], self.headers,self.sale_caseid,self.caseid

    # 撤销出售合同状态
    def cancel_contract_status(self,deal_id,status,content="需要撤销对应的合同审核状态"):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/erpWeb/managerCenter/contract/updateMgrDealAduitStatusByCounter"
        data = {"dealId":deal_id,"dealType":"101","dealAuditStatus":status,"dealVerifyCon":content}

        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]

    # 合同作废
    def delete_contract(self,deal_id,status="3",content="该合同需要作废处理"):
        headers = add_clientkey_to_headers.get_clientkey()
        url = "http://hft.myfun7.com/erpWeb/managerCenter/contract/updateMgrDealAduitStatus"
        data = {"dealId": deal_id, "dealType": "101", "dealAuditStatus": status, "dealVerifyCon": content}

        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["errCode"]




