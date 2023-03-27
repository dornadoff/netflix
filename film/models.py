from django.db import models
from django.core.validators import MinValueValidator, ValidationError
from django.contrib.auth.models import User

def validate_davlat(davlat):
    davlatlar = ["O'zbekiston", "AQSh", "Angliya", "Xitoy"]
    if davlat not in davlatlar:
        raise ValidationError("Bu davlatdan aktyor saqlash mumkin emas!")

class Aktyor(models.Model):
    ism = models.CharField(max_length=100)
    tugilgan_yili = models.DateField()
    jins = models.CharField(max_length=10)
    davlat = models.CharField(max_length=100, validators=[validate_davlat])
    def __str__(self):
        return f"{self.id}. {self.ism}"

class Kino(models.Model):
    nom = models.CharField(max_length=1000)
    yil = models.DateField()
    janr = models.CharField(max_length=100)
    aktyorlar = models.ManyToManyField(Aktyor)
    def __str__(self):
        return self.nom

class Tarif(models.Model):
    nom = models.CharField(max_length=100)
    narx = models.PositiveIntegerField(validators=[MinValueValidator(3)])
    muddat = models.CharField(max_length=30)
    def __str__(self):
        return self.nom

class Izoh(models.Model):
    matn = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kino = models.ForeignKey(Kino, on_delete=models.CASCADE)
    sana = models.DateField()
