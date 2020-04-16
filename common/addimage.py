
import requests
from config import JPG_PATH
from common import login_get_clientkey
import json


class AddImg():
    def sendImg(self, jpgpath,jpgtype='image/jpeg'):
        url = 'http://hft.myfun7.com/erpWeb/common/fileUpload'
        headers={}
        #获取CLIENTKEY
        headers.update({'CLIENTKEY':login_get_clientkey.login()})
        # print(headers)

        #获取需要上传的图片
        body={'hftPic': ('1.jpg',open(jpgpath, 'rb'),jpgtype)}

        #发起请求
        r = requests.post(url, files=body,headers=headers)

        # 解决抛异常
        try:
            jpg_path = r.json()['data']['filePath']    # 获取图片相对路径
            print(jpg_path)
            return jpg_path

        except Exception as msg:    # 返回报错信息
            print('图片上传失败，原因：%s'%msg)   # 打印报错信息
        #   raise   # 主动抛原始异常
        #   raise  ··· # 抛出异常内容为：“···”
            return ''

# if __name__=='__main__':
#     # s = requests.session()
#     # 调登录方法
#     login_get_clientkey.login()
#     # 上传文件
#     send = AddImg()                 # 把类sendfile()实例化为对象
#     send.sendImg(JPG_PATH)          # 调用sendfile()里面的sendImg方法