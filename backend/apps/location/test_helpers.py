from apps.location.models import (
    Continent,
    Country,
    State,
    County,
    City,
    Neighborhood,
    StreetType,
    Street
)

continent = Continent(name="America")

brazil = Country(
    continent=continent,
    name="Brazil",
    code="BR"
)

argentina = Country(
    continent=continent,
    name="Argentina",
    code="AR"
)

united_states = Country(
    continent=continent,
    name="United States",
    code="US"
)

germany = Country(
    continent=continent,
    name="Germany",
    code="DE"
)

portugal = Country(
    continent=continent,
    name="Portugal",
    code="PT"
)

sao_paulo_state = State(
    country=brazil,
    name="São Paulo",
    type="S"
)

buenos_aires_province = State(
    country=argentina,
    name="Buenos Aires",
    type="P"
)

buenos_aires_county = County(
    state=buenos_aires_province,
    name="Buenos Aires",
    type="C"
)

sao_paulo_district = County(
    state=sao_paulo_state,
    name="São Paulo",
    type="D"
)

sao_paulo_city = City(
    county=sao_paulo_district,
    name="São Paulo",
    type="C"
)

san_isidro_city = City(
    county=buenos_aires_county,
    name="San Isidro",
    type="C"
)

lapa = Neighborhood(
    country=sao_paulo_city,
    name="São Paulo",
    type="N"
)

acasusso_neighborhood = Neighborhood(
    country=san_isidro_city,
    name="Acassuso",
    type="N"
)

street = StreetType(name="Street")

acassuso = Street(
    neighborhood=acasusso_neighborhood,
    name="Acassuso",
    type=street,
    postal_code="1641"
)

croata = Street(
    neighborhood=lapa,
    name="Croata",
    type=street,
    postal_code="05056-020"
)