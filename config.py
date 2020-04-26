import os
BASE_PATH=os.path.dirname(os.path.abspath(__file__))
# print(BASE_PATH)

CASE_PATH=os.path.join(BASE_PATH,'case')
# print(CASE_PATH)

REPORT_PATH=os.path.join(BASE_PATH,'report')
# print(REPORT_PATH)

DATA_PATH=os.path.join(BASE_PATH,"datas")

HOUSE_MANAGE_EXCEL_PATH=os.path.join(DATA_PATH,"HouseManage_test_datas.xlsx")
# print(EXCEL_PATH)
CUSTOMER_MANAGE_EXCEL_PATH=os.path.join(DATA_PATH,"CustomerManage_test_datas.xlsx")



COMMON_PATH=os.path.join(BASE_PATH,"common")


# TEST_REPORT=os.path.join(COMMON_PATH,"testreport.xlsx")

RESULT_PATH=os.path.join(REPORT_PATH,"result.xlsx")

IMGDATA_PATH=os.path.join(BASE_PATH,"imgdata")
# print(IMGDATA_PATH)

JPG_PATH=os.path.join(IMGDATA_PATH,"1.jpg")
# print(JPG_PATH)

# s = '\xe9\x9d\x92\xe8\x9b\x99\xe7\x8e\x8b\xe5\xad\x90'
# ss = s.encode('raw_unicode_escape')
# print(ss)
# sss = ss.decode()
# print(sss)


# import ddt
# import unittest
# data = [
#     {'user':'11','psw':'1111'},
#     {'user':'22','psw':'2222'},
#     {'user':'33','psw':'3333'}
# ]
# @ddt.ddt
# class Test(unittest.TestCase):
#     @ddt.data(*data)
#     #@ddt.data({'user':'11','psw':'1111'},
#               #{'user':'22','psw':'2222'},
#               #{'user':'33','psw':'3333'})
#     def test_login(self, a):
#         #使用参数a来接收数据
#         print(a)
#         print(a['user'],a['psw'])
#
# if __name__ == '__main__':
#     unittest.main()