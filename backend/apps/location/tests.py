from django.test import TestCase
from apps.location import test_helpers
from apps.location.models import *

class TestLocation(TestCase):
    def setUp(self):
        continent = Continent.objects.create(name="America")

        brazil = Country.objects.create(
            continent=continent,
            name="Brazil",
            code="BR"
        )

        argentina = Country.objects.create(
            continent=continent,
            name="Argentina",
            code="AR"
        )

        united_states = Country.objects.create(
            continent=continent,
            name="United States",
            code="US"
        )

        germany = Country.objects.create(
            continent=continent,
            name="Germany",
            code="DE"
        )

        portugal = Country.objects.create(
            continent=continent,
            name="Portugal",
            code="PT"
        )

        sao_paulo_state = State.objects.create(
            country=brazil,
            name="São Paulo",
            type="S"
        )

        buenos_aires_province = State.objects.create(
            country=argentina,
            name="Buenos Aires",
            type="P"
        )

        buenos_aires_county = County.objects.create(
            state=buenos_aires_province,
            name="Buenos Aires",
            type="C"
        )

        sao_paulo_district = County.objects.create(
            state=sao_paulo_state,
            name="São Paulo",
            type="D"
        )

        sao_paulo_city = City.objects.create(
            county=sao_paulo_district,
            name="São Paulo",
            type="C"
        )

        san_isidro_city = City.objects.create(
            county=buenos_aires_county,
            name="San Isidro",
            type="C"
        )

        lapa = Neighborhood.objects.create(
            country=sao_paulo_city,
            name="São Paulo",
            type="N"
        )

        acasusso_neighborhood = Neighborhood.objects.create(
            country=san_isidro_city,
            name="Acassuso",
            type="N"
        )

        street = StreetType.objects.create(name="Street")

        acassuso = Street.objects.create(
            neighborhood=acasusso_neighborhood,
            name="Acassuso",
            type=street,
            postal_code="1641"
        )

        croata = Street.objects.create(
            neighborhood=lapa,
            name="Croata",
            type=street,
            postal_code="05056-020"
        )
    
    def test_continent(self):
        assert Continent.objects.last().name.lower() == "america"