

import random

class CreatePhone(object):

    def create_phone(self):
        head_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                    "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                    "180","181","182","183","185","186", "187", "188", "189"]
        #随机取手机号开头的三位数
        first_phone = random.choice(head_list)

        # 选取手机号的后8为数字
        end_phone = "".join(random.choice("0123456789") for i in range(8))

        return first_phone + end_phone