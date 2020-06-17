

import random,requests,json,pymssql
from common import readexcel,login_get_clientkey
from config import *

# 随机生成手机号
class CreatePhone(object):
    def create_phone(self):
        head_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                    "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                    "180","181","182","183","185","186", "187", "188", "189"]
        #随机取手机号开头的三位数
        first_phone = random.choice(head_list)

        # 选取手机号的后8为数字
        end_phone = "".join(random.choice("0123456789") for i in range(8))

        return first_phone + end_phone

# 创建支付接口
class Payment():
    def create_paymentTask(self,money):
        clientkey = login_get_clientkey.login()
        header = readexcel.ExcelUtil(USER_MANAGE_EXCEL_PATH,sheetName="创建充值金额接口").dict_data()[0]
        headers = json.loads(header["headers"])
        headers["CLIENTKEY"] = clientkey

        url="http://admin.myfun7.com/adminWeb/payment/cashRecharge/createPaymentTask"
        data={"deptId":"293846",
              "cityId":"1","archiveId":"1336698",
              "payModel":"1","isRechargeComp":"0","totalMoney": money}
        r=requests.post(url,headers=headers, data=data)
        return r.json()["data"]["ptId"], r.json()["data"]["token"]


# 连接数据库
class ConnectDataBase():
    # 连接数据库，获取用户名和密码
    def get_userAddPwd(self):
        connect = pymssql.connect(host="172.16.12.60:23456",user="s_dev",password="test@258369",database="hft_erpdb_CD",charset="UTF-8")
        cursors=connect.cursor()
        sql = "SELECT USER_NAME,LOGIN_PASSWORD from FUN_USERS;"
        cursors.execute(sql)
        result=cursors.fetchall()
        print(result)
        print(type(result))
        lst=[]
        for i in result:
            if i[1]:
                lst.append(i)
                print(i)
        cursors.close()
        connect.close()
        return lst
#
# a=ConnectDataBase().get_userAddPwd()
# print(a)



