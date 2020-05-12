


import unittest,json,ddt
from common import readexcel,add_clientkey_to_headers,base_api
from config import *
import requests

@ddt.ddt
class ModifyPwd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        cls.header = add_clientkey_to_headers.get_clientkey()
    def tearDown(self):
        #将密码重置为修改前的密码
        url="http://hft.myfun7.com/erpWeb/usercenter/modifyPwd"
        header=self.header
        data={"loginPassword":"hejun1130","oldLoginPassword":self.data_pwd}
        re = requests.post(url=url, headers=header, json=data)
        if re.json()["errCode"] == 200:
            print("密码重置成功")
        else:
            print("密码重置失败")

    testdata = readexcel.ExcelUtil(HOUSE_MANAGE_EXCEL_PATH, sheetName="修改密码").dict_data()
    @ddt.data(*testdata)
    def test_modify_pwd(self,data):
        data["headers"]=self.header
        res = base_api.send_requests(self.s, data)

        # 检查点 checkpoint
        check = data["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # json字符串转为字典
        str_pwd=data["body"]
        pwd_data=json.loads(str_pwd)
        self.data_pwd=pwd_data["loginPassword"]
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res["text"]  # 获取响应的内容
        res_text = json.loads(res_text)  # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        #断言
        self.assertEqual(check.get("errCode"),res_text["errCode"])


if __name__ == '__main__':
    unittest.main()