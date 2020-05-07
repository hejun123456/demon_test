# from common.HTMLTestRunner_api import *
#
# cases = add_case()
# run_case(cases)


class Add():
    def add(self):
        a=3+2
        return a


def get():
    lst = []
    for i in range(4):
        caseid = Add().add()
        b = caseid
        lst.append(b)
        print(lst)
    return lst

b=get()
# print(b)