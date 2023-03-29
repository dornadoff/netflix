from film.serializers import *
from unittest import TestCase

class TestAktyorSerializer(TestCase):
    def test_aktyor(self):
        aktyor = {"ism":"Dwayne Johnson",
                  "davlat": "USA",
                  "jins": "erkak",
                  "tugilgan_yili":"1972-05-02"}
        serializer = AktyorSeializer(data=aktyor)
        # assert serializer.is_valid() == True
        self.assertTrue(serializer.is_valid() == True)
        # self.assertEqual(serializer.is_valid, True)
        malumot = serializer.validated_data
        print(malumot)
        assert malumot.get('davlat') == "USA"
        assert malumot.get('ism') == "Dwayne Johnson"
        assert malumot.get('jins') == "erkak"

    def test_invalid_aktyor(self):
        aktyor = {"ism":"Ol",
                  "davlat": "USA",
                  "jins": "adfasf",
                  "tugilgan_yili":"1972-05-02"}
        serializer = AktyorSeializer(data=aktyor)
        assert serializer.is_valid() == False
        assert serializer.errors['ism'][0] == "Ism bunaqa kalta bo'lmaydi"
        assert serializer.errors['jins'][0] == "Bunday jins yoq"
