from apps.location.models import Street
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
    document = models.TextField(max_length=50)

    def __str__(self):
        return self.name
    
class AddressType(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name
    
class PersonAddress(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    address_type = models.ForeignKey(AddressType, on_delete=models.PROTECT) # home, work...
    street = models.ForeignKey(Street, on_delete=models.PROTECT)
    number = models.IntegerField()
    complement = models.TextField(max_length=150)

    def __str__(self):
        return f"{self.person.name}@{self.address_type.name}"