from rest_framework import serializers
from .models import *

class AktyorSeializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ism = serializers.CharField(max_length=100)
    tugilgan_yili = serializers.DateField()
    jins = serializers.CharField(max_length=10)
    davlat = serializers.CharField(max_length=100)

    def validate_ism(self, qiymat):
        if len(qiymat) < 3:
            raise serializers.ValidationError("Ism bunaqa kalta bo'lmaydi")
        return qiymat

    def validate_jins(self, qiymat):
        if qiymat != "erkak" and qiymat != "ayol":
            raise serializers.ValidationError("Bunday jins yoq")
        return qiymat

class TarifSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nom = serializers.CharField(max_length=100)
    narx = serializers.IntegerField()
    muddat = serializers.CharField(max_length=30)

class KinoSerializer(serializers.ModelSerializer):
    aktyorlar = AktyorSeializer(many=True)
    class Meta:
        model = Kino
        fields = "__all__"

class KinoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = "__all__"

class IzohSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = "__all__"