

import requests,json
from common import readexcel
from config import *
from common import add_clientkey_to_headers

class WageManage():
    def delete_wageRoleConfig(self,headers,id,baseWage="0",roleId="59fa1fa4e7b84d5c867458f02e4cb8ec"):
        url="http://hft.myfun7.com/erpWeb/managecenter/profit/updateRoleWageConfig"
        data = {"id": id,
                "baseWage": baseWage,
                "roleId": roleId}
        r=requests.post(url,headers=headers,json=data)
        return r.json()["errCode"]


