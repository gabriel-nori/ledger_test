from apps.location.models import (
    Continent,
    Country,
    State,
    County,
    City,
    Neighborhood,
    StreetType,
    Street,
)


class TestObjects:
    continent = None
    brazil = None
    argentina = None
    united_states = None
    germany = None
    portugal = None
    sao_paulo_state = None
    buenos_aires_province = None
    buenos_aires_county = None
    sao_paulo_district = None
    sao_paulo_city = None
    san_isidro_city = None
    lapa = None
    acasusso_neighborhood = None
    street = None
    acassuso = None
    croata = None

    def create(self):
        self.continent = Continent.objects.get_or_create(name="America")[0]

        self.brazil = Country.objects.get_or_create(
            continent=self.continent, name="Brazil", code="BR"
        )[0]

        self.argentina = Country.objects.get_or_create(
            continent=self.continent, name="Argentina", code="AR"
        )[0]

        self.united_states = Country.objects.get_or_create(
            continent=self.continent, name="United States", code="US"
        )[0]

        self.germany = Country.objects.get_or_create(
            continent=self.continent, name="Germany", code="DE"
        )[0]

        self.portugal = Country.objects.get_or_create(
            continent=self.continent, name="Portugal", code="PT"
        )[0]

        self.sao_paulo_state = State.objects.get_or_create(
            country=self.brazil, name="São Paulo", type="S"
        )[0]

        self.buenos_aires_province = State.objects.get_or_create(
            country=self.argentina, name="Buenos Aires", type="P"
        )[0]

        self.buenos_aires_county = County.objects.get_or_create(
            state=self.buenos_aires_province, name="Buenos Aires", type="C"
        )[0]

        self.sao_paulo_district = County.objects.get_or_create(
            state=self.sao_paulo_state, name="São Paulo", type="D"
        )[0]

        self.sao_paulo_city = City.objects.get_or_create(
            county=self.sao_paulo_district, name="São Paulo", type="C"
        )[0]

        self.san_isidro_city = City.objects.get_or_create(
            county=self.buenos_aires_county, name="San Isidro", type="C"
        )[0]

        self.lapa = Neighborhood.objects.get_or_create(
            country=self.sao_paulo_city, name="São Paulo", type="N"
        )[0]

        self.acasusso_neighborhood = Neighborhood.objects.get_or_create(
            country=self.san_isidro_city, name="Acassuso", type="N"
        )[0]

        self.street = StreetType.objects.get_or_create(name="Street")[0]

        self.acassuso = Street.objects.get_or_create(
            neighborhood=self.acasusso_neighborhood,
            name="Acassuso",
            type=self.street,
            postal_code="1641",
        )[0]

        self.croata = Street.objects.get_or_create(
            neighborhood=self.lapa,
            name="Croata",
            type=self.street,
            postal_code="05056-020",
        )[0]
