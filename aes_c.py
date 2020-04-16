#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @DATE:2019/8/1
# @Author  : shl
# @File    : aes_c.py
# @DESC    : 略
import ctypes


class AesHelper(object):
    def __init__(self):
        self.c_lib = ctypes.cdll.LoadLibrary("AESMethod.dll")
        self.c_type = ctypes.c_char_p

    def encrypt(self, e_parm):
        """
        加密 调取c++
        :return:
        """
        aesEncode = self.c_lib.aesEncode
        aesEncode.restype = self.c_type

        return aesEncode(e_parm)

    def decrypt(self, de_parm):
        """
        解密
        :param de_parm:
        :return:
        """
        aesDecode = self.c_lib.aesDecode
        aesDecode.restype = self.c_type
        return aesDecode(de_parm)


def start1():
    load_dll = ctypes.cdll.LoadLibrary
    lib = load_dll("AESMethod.dll")
    aesEncode = lib.aesEncode
    aesEncode.restype = ctypes.c_char_p
    reStr = aesEncode('{"cityId": 1,"sId": 854598}')
    print (reStr)
    aesDecode = lib.aesDecode
    aesDecode.restype = ctypes.c_char_p
    reStr2 = aesDecode(reStr)
    print (reStr2)


def start():
    aes_util = AesHelper()
    e_str = '{"cityId":"1","sId":"1626773"}'
    print(u'参数：{0} 加密：{1}'.format(e_str, aes_util.encrypt(e_str)))
    de_str = '707D094510F3A54B53D4EA80BB5BF714C0B43542C9F4E79EA2D2645D3A78F8FF'
    print(u'参数：{1} 解密：{0}'.format(aes_util.decrypt(de_str), de_str))




if __name__ == '__main__':
    start()
