from django.db import models


class Continent(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Country(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.PROTECT)
    name = models.TextField(max_length=50)
    code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class State(models.Model):
    TYPES = [("S", "State"), ("P", "Province")]
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.TextField(max_length=50)
    type = models.CharField(choices=TYPES, default="S", max_length=1)

    def __str__(self):
        return self.name


class County(models.Model):
    TYPES = [("C", "County"), ("D", "District")]
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    name = models.TextField(max_length=50)
    type = models.CharField(choices=TYPES, default="C", max_length=1)

    def __str__(self):
        return self.name


class City(models.Model):
    TYPES = [("C", "City"), ("T", "Town")]
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    name = models.TextField(max_length=50)
    type = models.CharField(choices=TYPES, default="C", max_length=1)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    TYPES = [("N", "Neighborhood"), ("C", "Community")]
    country = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.TextField(max_length=50)
    type = models.CharField(choices=TYPES, default="N", max_length=1)

    def __str__(self):
        return self.name


class StreetType(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Street(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.PROTECT)
    name = models.TextField(max_length=50)
    type = models.ForeignKey(StreetType, on_delete=models.PROTECT)
    postal_code = models.TextField()

    def __str__(self):
        return self.name
