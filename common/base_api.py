# coding:utf-8
# 作者：hejun


import json
import requests
from common.readexcel import ExcelUtil
from common.writeexcel import copy_excel, Write_excel
from config import *
import time

def send_requests(s,testdata):
    # 封装requests请求方法
    method = testdata["method"]
    url = testdata["url"]
    # url后面的params参数
    try:
         params = eval(testdata["params"])
    except:
         params = None
     # 请求头部headers
    try:
         # print(testdata)
         # headers = eval(testdata["headers"])
         if not isinstance(testdata["headers"], dict):
             headers = json.loads(testdata["headers"])
         # headers = eval(testdata["headers"])
         else:
             headers = testdata["headers"]
         print("请求头部：%s" % headers)
    except Exception as e:
         print(e)
         headers = None
    # post请求body类型
    types = testdata["type"]
    test_nub = testdata['id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)
    print("请求headers: %s" %headers)

     # post请求body内容
    try:
         bodydata = testdata["body"]
         # print("1111111")
         # print(type(bodydata))
         bodydata=bodydata.rstrip("/n")
    except:
         bodydata = {}

     # 判断数据传的是data还是json
    if types == "data":
         body = bodydata
         body=body.encode("utf-8")
         # print("000000000000")
         # print(body)
         # print(type(body))
    elif types == "json":
         body = json.dumps(bodydata)
    else:
         body = bodydata
    #判断请求方式
    if method == "post":
        # bodys=body.encode("utf-8")
        print("post请求body类型为：%s ,body内容为：%s" % (types,body))
    elif method == "get":
        print("get请求body类型为：%s ,body内容为：%s" % (types,body))
    elif method == "head":
        print("head请求body类型为：%s ,body内容为：%s" % (types,body))
    elif method == "put":
        print("put请求body类型为：%s ,body内容为：%s" % (types, body))
    elif method == "patch":
        print("patch请求body类型为：%s ,body内容为：%s" % (types, body))
    elif method == "delete":
        print("delete请求body类型为：%s ,body内容为：%s" % (types, body))
    elif method == "delete":
        print("delete请求body类型为：%s ,body内容为：%s" % (types, body))
    elif method == "options":
        print("options请求body类型为：%s ,body内容为：%s" % (types, body))

    verify = False
    res = {}   # 接受返回数据
    try:
         r = s.request(method=method,
                      url=url,
                       params=params,
                       headers=headers,
                       data=body,
                       verify=verify)
         # print(body)
         print("页面返回信息：%s" % r.content.decode("UTF-8"))
         res['id'] = testdata['id']
         res['rowNum'] = testdata['rowNum']
         res["statuscode"] = str(r.status_code)        # 状态码转成str
         res["text"] = r.content.decode("UTF-8")
         res["times"] = str(r.elapsed.total_seconds())    # 接口请求时间转str
         if res["statuscode"] != "200":
            res["error"] = res["text"]
         else:
            res["error"] = ""
         res["msg"] = ""
         if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
         else:
             res["result"] = "fail"
         return res
    except Exception as msg:
         res["msg"] = str(msg)
         return res

def wirte_result(res, filename=RESULT_PATH):
     # 返回结果的行数row_nub
     row_nub = res['rowNum']
     print(row_nub)
     # 写入statuscode
     wt = Write_excel(filename)
     wt.write(row_nub, 10, res['statuscode'])        # 写入返回状态码statuscode,第10列
     wt.write(row_nub, 11, res['times'])             # 耗时
     wt.write(row_nub, 12, res['error'])            # 状态码非200时的返回信息
     wt.write(row_nub, 14, res['result'])           # 测试结果 pass 还是fail
     wt.write(row_nub, 15, res['msg'])              #抛异常

# if __name__ == "__main__":
#     data = ExcelUtil(EXCEL_PATH,sheetName="登录接口").dict_data()
#     print(data[0])
#     s = requests.session()
#     res = send_requests(s, data[0])
#     print(res)
    # copy_excel(EXCEL_PATH, RESULT_PATH)
    # wirte_result(res, filename=RESULT_PATH)