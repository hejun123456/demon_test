


from common.FunSoSo import FunSoSo
import unittest


class SoSoSale_Addto_HouseManage(unittest.TestCase):
    def setUp(self):
        self.data=FunSoSo()
        self.datas,self.ids=self.data.get_sosoSale_infoById()
        self.a=self.datas.get("id")

    def test_soso_to_HouseManage(self):

        self.assertEqual(str(self.a),self.ids)

if __name__ == "__main__":
     unittest.main()
