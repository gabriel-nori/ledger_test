from apps.person.test_helpers import TestObjects
from apps.person import utils as personUtils
from datetime import date, timedelta
from django.test import TestCase


class PersonTest(TestCase):
    def setUp(self):
        self.test_objects = TestObjects()
        self.test_objects.create()

    def test_age(self):
        """
        To open a bank account, one must be older (or exactly) 16 years old.
        In this case, our client can't be younger than 16 years.
        """

        assert self.test_objects.underage_client.birthday >= date.today() - timedelta(
            days=16 * 365
        )
        assert self.test_objects.michael_ok.birthday <= date.today() - timedelta(
            days=16 * 365
        )

    def test_age_validators(self):
        """
        Let's check if the validators are working correctly to check if the client is older than 16 and/or older than 18
        """
        assert not personUtils.check_16_older(
            self.test_objects.underage_client.birthday
        )
        assert not personUtils.check_18_older(
            self.test_objects.underage_client.birthday
        )
        assert personUtils.check_16_older(self.test_objects.michael_ok.birthday)
        assert personUtils.check_18_older(self.test_objects.michael_ok.birthday)
