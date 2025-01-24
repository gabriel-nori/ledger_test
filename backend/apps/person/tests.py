from apps.person.models import Person, Occupation
from django.test import SimpleTestCase
from datetime import date, timedelta
from apps.person import utils as personUtils
import mock

class PersonTest(SimpleTestCase):
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
