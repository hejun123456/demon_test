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

ORGANIZATION_MANAGE_EXCEL_PATH=os.path.join(DATA_PATH,"OrganizationManage_test_datas.xlsx")

SOSO_EXCEL_PATH=os.path.join(DATA_PATH,"HaoFang_SoSo_test_datas.xlsx")

COMMON_PATH=os.path.join(BASE_PATH,"common")


# TEST_REPORT=os.path.join(COMMON_PATH,"testreport.xlsx")

RESULT_PATH=os.path.join(REPORT_PATH,"result.xlsx")

IMGDATA_PATH=os.path.join(BASE_PATH,"imgdata")
# print(IMGDATA_PATH)

JPG_PATH=os.path.join(IMGDATA_PATH,"1.jpg")
# print(JPG_PATH)


