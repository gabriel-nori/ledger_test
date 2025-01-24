from apps.person.models import Person, Occupation
from datetime import date

child_occupation = Occupation(name="child")
occupation = Occupation(name="tester")
underage_client = Person(
    name="john doe",
    birthday=date(2021, 12, 21),
    sex="F",
    gender="F",
    primary_email="teste@teste.com",
    occupation=child_occupation,
    document="ajbsjbajsbas"
)

approved_client = Person(
    name="Michael Kyle",
    birthday=date(1960, 9, 4),
    sex="M",
    gender="M",
    primary_email="teste@teste.com",
    occupation=occupation,
    document="ajbsjbajsbas"
)

fernando_ok = Person(
    name="Fernando",
    birthday=date(1990, 12, 5),
    sex="M",
    gender="M",
    primary_email="teste@teste.com",
    occupation=occupation,
    document="ajbsjbajsbas"
)

maria_ok = Person(
    name="Michael Kyle",
    birthday=date(2000, 1, 27),
    sex="F",
    gender="F",
    primary_email="teste@teste.com",
    occupation=occupation,
    document="ajbsjbajsbas"
)