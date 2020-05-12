

import requests,json
from common import base_api,readexcel
from config import *


#写一个退出系统方法
def Logout(clientkey):
    s = requests.session()
    data = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="退出系统").dict_data()
    header_data = data[0]["headers"]
    a=json.loads(header_data)
    a["CLIENTKEY"]=clientkey
    b=json.dumps(a)
    data[0].update({"headers":b})

    res=base_api.send_requests(s, data[0])
    res_text = res["text"]           #获取返回的值
    res_texts=json.loads(res_text)   #将返回的值转化为字典
    result_data=res_texts.get("DATA")[0]["RESULT"]
    if result_data == "SUCCESS":
        print("退出系统状态:%s" %(result_data))
    else:
        print("退出系统状态:%s" %(result_data))