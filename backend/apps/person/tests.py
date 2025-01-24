from apps.person.models import Person, Occupation
from apps.person import utils as personUtils
from datetime import date, timedelta
from django.test import TestCase

class PersonTest(TestCase):
    def setUp(self):
        self.child_occupation = Occupation.objects.create(name="child")
        self.occupation = Occupation.objects.create(name="tester")
        self.underage_client = Person.objects.create(
            name="john doe",
            birthday=date(2021, 12, 21),
            sex="F",
            gender="F",
            primary_email="teste@teste.com",
            occupation=self.child_occupation,
            document="john"
        )

        self.approved_client = Person.objects.create(
            name="Michael Kyle",
            birthday=date(1960, 9, 4),
            sex="M",
            gender="M",
            primary_email="michael@teste.com",
            occupation=self.occupation,
            document="michael"
        )

        self.fernando_ok = Person.objects.create(
            name="Fernando",
            birthday=date(1990, 12, 5),
            sex="M",
            gender="M",
            primary_email="fernando@teste.com",
            occupation=self.occupation,
            document="fernando"
        )

        self.maria_ok = Person.objects.create(
            name="Michael Kyle",
            birthday=date(2000, 1, 27),
            sex="F",
            gender="F",
            primary_email="maria@teste.com",
            occupation=self.occupation,
            document="maria"
        )

    def test_age(self):
        """
        To open a bank account, one must be older (or exactly) 16 years old.
        In this case, our client can't be younger than 16 years.
        """

        assert self.underage_client.birthday >= date.today()-timedelta(days=16*365)
        assert self.approved_client.birthday <= date.today()-timedelta(days=16*365)

    def test_age_validators(self):
        """
        Let's check if the validators are working correctly to check if the client is older than 16 and/or older than 18
        """
        assert not personUtils.check_16_older(self.underage_client.birthday)
        assert not personUtils.check_18_older(self.underage_client.birthday)
        assert personUtils.check_16_older(self.approved_client.birthday)
        assert personUtils.check_18_older(self.approved_client.birthday)
