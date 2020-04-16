import unittest




from common.addimage import AddImg
from config import JPG_PATH


jpgpath=JPG_PATH

class TestSendFile(unittest.TestCase):
    def test_file_upload(self):
        self.login = AddImg()
        result=self.login.sendImg(jpgpath)    #发送图片

        self.assertIn('.jpg', result)          #断言

# if __name__=="main":
#     unittest.main()
