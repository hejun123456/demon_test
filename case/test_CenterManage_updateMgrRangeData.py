# coding:utf-8
# 作者：hejun


import unittest, ddt
import requests, json
from common import base_api, OrganizationManage
from common import readexcel
from config import *

# 读取出excel中的测试数据
testdata = readexcel.ExcelUtil(ORGANIZATION_MANAGE_EXCEL_PATH, sheetName="组织管理-员工档案-更新片区").dict_data()
print(testdata)

@ddt.ddt
class UpdateMgrRangeData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 保持登录状态
        cls.s = requests.session()
        cls.area1_id, cls.header = OrganizationManage.OrganizationManage().insert_mgr_area()   # 增加大区

    def setUp(self):
        # 增加一个片区
        url="http://hft.myfun7.com/erpWeb/managerCenter/organization/insertMgrRangeData"
        data={"areaId":self.area1_id,"regName":"自动化测试片区"}
        r=requests.post(url,headers=self.header,json=data)
        self.reg_id=r.json()["data"]["regId"]

    @ddt.data(*testdata)
    def test_update_mgr_rangeData(self,case):
        a = json.loads(case["body"])
        case["headers"] = self.header
        a["regId"] = self.reg_id
        b = json.dumps(a)
        case.update({"body": b})

        res = base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        # 断言
        self.assertEqual(check.get("errCode"), res_text["errCode"])

    def tearDown(self):
        # 删除片区
        code=OrganizationManage.OrganizationManage().delete_insert_mgr_range(self.reg_id,self.header)
        if code == 200:
            print("片区成功删除")
        else:
            print("片区删除失败")

    @classmethod
    def tearDownClass(cls):
        # 删除大区
        code=OrganizationManage.OrganizationManage().delete_insert_mgr_area(cls.area1_id)
        if code == 200:
            print("大区成功删除")
        else:
            print("大区删除失败")

if __name__ == "__main__":
    unittest.main()