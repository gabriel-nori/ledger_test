from django.test import SimpleTestCase
from datetime import date, timedelta
from apps.person import utils as personUtils
from apps.person import test_helpers

class PersonTest(SimpleTestCase):
    def test_age(self):
        """
        To open a bank account, one must be older (or exactly) 16 years old.
        In this case, our client can't be younger than 16 years.
        """

        assert test_helpers.underage_client.birthday >= date.today()-timedelta(days=16*365)
        assert test_helpers.approved_client.birthday <= date.today()-timedelta(days=16*365)

    def test_age_validators(self):
        """
        Let's check if the validators are working correctly to check if the client is older than 16 and/or older than 18
        """
        assert not personUtils.check_16_older(test_helpers.underage_client.birthday)
        assert not personUtils.check_18_older(test_helpers.underage_client.birthday)
        assert personUtils.check_16_older(test_helpers.approved_client.birthday)
        assert personUtils.check_18_older(test_helpers.approved_client.birthday)
