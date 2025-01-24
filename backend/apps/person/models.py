from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Occupation(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name

class Person(models.Model):
    SEX_CHOICES = [("M", "Male"), ("F", "Female")]
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("X", "Nonbinary")
    ]
    name = models.TextField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    primary_email = models.TextField(max_length=320, null=True, blank=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
class AddressType(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name
    
class StreetType(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name
    
class PersonAddress(models.Model):
    """
        This is a simplified way of representing a normalized address.
        If I was going to develop a fully optimized system, the tables should be
        organized hierarchically more like a Geographic database
    """
    street_type = models.ForeignKey(StreetType, on_delete=models.PROTECT)
    street = models.TextField()