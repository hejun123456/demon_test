# coding:utf-8
# 作者：hejun

import requests, json
from common.base_api import send_requests
from common.readexcel import ExcelUtil
from config import *


def login():
    data = ExcelUtil(EXCEL_PATH, sheetName="获取clientkey").dict_data()
    print(data[0])
    s = requests.session()
    res = send_requests(s, data[0])
    # print(res)
    # 返回结果x
    res_text = res["text"]
    print(res_text)
    data_text = json.loads(res_text)

    client_key = data_text["DATA"][0]["OPERATOR"]["CLIENTKEY"]   #获取clientkey
    return client_key

# a=login()
# print(a)