from unittest import TestCase
from film.models import *
from rest_framework.test import APIClient

class TestAktyorAPI(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_aktyorlar(self):
        natija = self.client.get("/aktyorlar/")
        assert natija.status_code == 200
        aktyorlar = natija.data
        assert len(aktyorlar) == Aktyor.objects.all().count()
        assert aktyorlar[0]["ism"] == Aktyor.objects.first().ism

    def test_aktyor_valid(self):
        natija = self.client.get("/aktyor/3/")
        assert natija.status_code == 200
        assert natija.data["id"] == 3
        assert natija.data["ism"] == Aktyor.objects.get(id=3).ism
        assert natija.data["davlat"] == Aktyor.objects.get(id=3).davlat

    def test_aktyor_invalid(self):
        natija = self.client.get("/aktyor/29/")
        assert natija.status_code == 200
        assert natija.data["xabar"] == "Bunday id da aktyor yo'q"

    def test_aktyor_qoshish_invalid(self):
        aktyor = {
            "id": 10,
            "ism": "Akmal",
            "tugilgan_yili": "2007-01-01",
            "jins": "asdfas",
            "davlat": "Qirg'iziston"
        }
        natija = self.client.post("/aktyorlar/", data=aktyor)
        assert natija.status_code == 400
        assert natija.data['jins'][0] == "Bunday jins yoq"

    # def test_aktyor_qoshish(self):
    #     aktyor = {
    #         "id":23,
    #         "ism": "Akmal",
    #         "tugilgan_yili": "2007-01-01",
    #         "jins": "erkak",
    #         "davlat": "Qirg'iziston"
    #     }
    #     natija = self.client.post("/aktyorlar/", data=aktyor)
    #     assert natija.status_code == 201
    #     # assert natija.data["id"] is not None
    #     assert natija.data['ism'] == Aktyor.objects.last().ism
    #     assert natija.data['davlat'] == Aktyor.objects.last().davlat
    #     assert natija.data["jins"] == Aktyor.objects.last().jins

    def test_aktyor_put(self):
        aktyor = {
            "id":22,
            "ism": "Akmal",
            "tugilgan_yili": "2007-01-01",
            "jins": "erkak",
            "davlat": "Qirg'iziston"
        }
        eski = Aktyor.objects.get(id=22)
        natija = self.client.put("/aktyor/22/", data=aktyor)
        assert natija.status_code == 202
        assert natija.data["ism"] == "Akmal" == Aktyor.objects.get(id=22).ism
        assert natija.data['jins'] == eski.jins

