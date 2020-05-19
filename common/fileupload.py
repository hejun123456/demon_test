



from common.addimage import AddImg
from config import JPG_PATH


jpgpath=JPG_PATH
#
class TestSendFile():
    def test_file_upload(self):
        self.login = AddImg()
        result=self.login.sendImg(jpgpath)    #发送图片
        print(result)
        return result


    def file_upload_5(self):
        list_jpg = []
        for i in range(5):
            login = AddImg()
            result=login.sendImg(jpgpath)
            list_jpg.append(result)
        print(list_jpg)
        return list_jpg


