# coding:utf-8
# 作者：hejun



import requests, json
from common.base_api import send_requests
from common.readexcel import ExcelUtil
from config import *


def get_clientkey():
    # global header
    # try:
    data = ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="获取clientkey").dict_data()
    print(data[0])
    s = requests.session()
    res = send_requests(s, data[0])
    # print(res)
    # 返回结果x
    res_text = res["text"]
    # print(res_text)
    data_text = json.loads(res_text)

    client_key = data_text["DATA"][0]["OPERATOR"]["CLIENTKEY"]   #获取clientkey
    # print(client_key)
    header = json.loads(data[0]['headers'])   #json转换成字典
    # print(header)
    # 添加CLIENTKEY到headers中去
    header.update({'CLIENTKEY': client_key})
    # except Exception as e:
    #     print(e)
    return header



