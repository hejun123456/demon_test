# coding:utf-8
# 作者：hejun


import unittest, ddt, requests, json,time
from common import readexcel, OrganizationManage, base_api
from config import *

testdata=readexcel.ExcelUtil(ORGANIZATION_MANAGE_EXCEL_PATH, sheetName="增加员工").dict_data()
@ddt.ddt
class AddCompInviteUser(unittest.TestCase):

    def setUp(self):
        # 添加邀请员工信息
        self.tup_data = OrganizationManage.OrganizationManage().add_InviteUserInfo()
        print(self.tup_data)
        # 获取邀请链接参数
        self.link_params = OrganizationManage.OrganizationManage().get_inviteLink(self.tup_data[4])
        print(self.link_params)
        # 获取邀请id
        self.invite_id=OrganizationManage.OrganizationManage().get_inviteUserId(self.link_params,self.tup_data[3])
    def tearDown(self):
        # 按关键字查询添加的员工
        time.sleep(3)     # 等待返回值
        data=OrganizationManage.OrganizationManage().get_UserListInfo(self.tup_data[5], self.tup_data[4])
        print(data)
        if "list" in data.keys():
            user_id = (OrganizationManage.OrganizationManage().get_UserListInfo(self.tup_data[5],self.tup_data[4]))["list"]["list"][0]["userId"]

            # 注销员工
            code = OrganizationManage.OrganizationManage().delete_user(user_id,self.tup_data[4])
            if code == 200:
                print("用户注销成功")
            else:
                print("用户注销失败:%s" %(code))
        else:
            print("不存在注销的用户")

    @ddt.data(*testdata)
    def test_addCompInviteUser(self, case):
        dic_data=json.loads(case["body"])
        print(dic_data)
        dic_data["param"]=self.link_params
        dic_data["regIds"]=self.tup_data[0]
        dic_data["sectionIds"]=self.tup_data[1]
        dic_data["serviceZone"]=self.tup_data[2]
        dic_data["inviteId"]=self.invite_id

        res=requests.post(url=case["url"],headers=json.loads(case["headers"]), data=dic_data)
        # res=base_api.send_requests(self.s, case)

        # 检查点 checkpoint
        check = case["checkpoint"]  # 获取检查点中的内容
        check = json.loads(check)  # json字符串转为字典
        print("检查点->：%s" % check)

        # 返回结果
        res_text = res.json()            # 将响应的内容转换为字典
        print("返回实际结果->：%s" % res_text)

        # 断言
        self.assertEqual(check.get("errCode"), res_text["errCode"])


if __name__ == "__main__":
    unittest.main()