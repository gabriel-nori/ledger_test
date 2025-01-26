from apps.person.models import Person, Occupation
from django.contrib.auth import get_user_model
from datetime import date


class TestObjects:
    child_occupation = None
    occupation = None
    underage_client = None
    approved_client = None
    fernando_ok = None
    maria_ok = None

    def create(self):
        self.child_occupation = Occupation.objects.get_or_create(name="child")[0]
        self.occupation = Occupation.objects.get_or_create(name="tester")[0]
        self.underage_client = Person.objects.get_or_create(
            name="john doe",
            birthday=date(2021, 12, 21),
            sex="F",
            gender="F",
            primary_email="teste@teste.com",
            occupation=self.child_occupation,
            document="ajbsjbajsbas",
            user=get_user_model().objects.get_or_create(username="test_user_1")[0],
        )[0]

        self.michael_ok = Person.objects.get_or_create(
            name="Michael Kyle",
            birthday=date(1960, 9, 4),
            sex="M",
            gender="M",
            primary_email="teste@teste.com",
            occupation=self.occupation,
            document="ajbsjbajsbas",
            user=get_user_model().objects.get_or_create(username="test_user_2")[0],
        )[0]

        self.fernando_ok = Person.objects.get_or_create(
            name="Fernando",
            birthday=date(1990, 12, 5),
            sex="M",
            gender="M",
            primary_email="teste@teste.com",
            occupation=self.occupation,
            document="ajbsjbajsbas",
            user=get_user_model().objects.get_or_create(username="test_user_3")[0],
        )[0]

        self.maria_ok = Person.objects.get_or_create(
            name="Michael Kyle",
            birthday=date(2000, 1, 27),
            sex="F",
            gender="F",
            primary_email="teste@teste.com",
            occupation=self.occupation,
            document="ajbsjbajsbas",
            user=get_user_model().objects.get_or_create(username="test_user_4")[0],
        )[0]
