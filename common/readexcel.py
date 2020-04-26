# coding:utf-8
# 作者：hejun


import xlrd
from config import *

class ExcelUtil():
    def __init__(self,EXCEL_PATH,sheetName="登录接口"):
        self.data=xlrd.open_workbook(EXCEL_PATH)
        self.table=self.data.sheet_by_name(sheetName)
        # 获取第一行作为key值
        self.keys=self.table.row_values(0)
        # 获取总行数
        self.rowNum=self.table.nrows
        # 获取总列数
        self.colNum=self.table.ncols


    def dict_data(self):
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            r=[]
            j=1
            for i in list(range(self.rowNum-1)):
                s={}
            # 从第二行取对应values值
                s['rowNum']=i+2
                values=self.table.row_values(j)
                for x in list(range(self.colNum)):
                    s[self.keys[x]]=values[x]
                r.append(s)
                j += 1
        return r

# if __name__=="__main__":
#     excelpath = HOUSE_MANAGE_EXCEL_PATH
#     sheetName = "服务器接口"
#     data = ExcelUtil(excelpath, sheetName)
#     print(data.dict_data())
