from apps.location.models import Country, Street
from apps.person.models import Person
from django.db import models


class InstitutionType(models.Model):
    name = models.TextField(
        max_length=50
    )  # Commercial banks, Credit unions, Investment banks, Insurance companies, Savings and loan associations...

    def __str__(self):
        return self.name


class Institution(models.Model):  # This is useful for multi country operation
    name = models.TextField(max_length=50)
    type = models.ForeignKey(InstitutionType, on_delete=models.PROTECT)
    code = models.CharField(max_length=5)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Branch(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    street = models.ForeignKey(Street, on_delete=models.PROTECT)
    number = models.IntegerField()
    floor = models.IntegerField(null=True, blank=True)
    room = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.institution.code}-{self.code}"


class BranchClient(models.Model):
    client = models.ForeignKey(Person, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    client_since = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.branch.code} - {self.client.name}"
