from apps.financial_institution.models import Branch
from apps.person.models import Person, Occupation
from apps.person import utils as personUtils
from django.contrib.auth import get_user_model
from apps.account.models import Account
from datetime import date, timedelta
from django.test import TestCase

class PersonTest(TestCase):
    def setUp(self):
        self.kyle_account = Account(
            account_holder=Person.objects.get_or_create(
                primary_email="michael@teste.com",
                defaults={
                    "name":"Michael Kyle",
                    "birthday":date(1960, 9, 4),
                    "sex":"M",
                    "gender":"M",
                    "primary_email":"michael@teste.com",
                    "occupation":Occupation.objects.get_or_create(name="developer")[0],
                    "document":"michael",
                    "user":get_user_model().objects.get_or_create(username="test0")[0]
                }
            )[0],
            institution_branch=Branch.objects.get(code="09832"),
            identifier="12121212",
            overdraft_protection=True,
            overdraft_limit=250000,
            balance=0
        )

        self.fernando_account = Account(
            account_holder=Person.objects.get_or_create(
                primary_email="michael@teste.com",
                defaults={
                    "name":"Fernando",
                    "birthday":date(1960, 9, 4),
                    "sex":"M",
                    "gender":"M",
                    "primary_email":"michael@teste.com",
                    "occupation":Occupation.objects.get_or_create(name="developer")[0],
                    "document":"michael",
                    "user":get_user_model().objects.get_or_create(username="test2")[0]
                }
            )[0],
            institution_branch=Branch.objects.get(code="12409"),
            identifier="12121212",
            overdraft_protection=True,
            overdraft_limit=250000,
            balance=0
        )

        self.maria_account = Account(
            account_holder=Person.objects.get_or_create(
                primary_email="michael@teste.com",
                defaults={
                    "name":"Maria",
                    "birthday":date(1960, 9, 4),
                    "sex":"M",
                    "gender":"M",
                    "primary_email":"michael@teste.com",
                    "occupation":Occupation.objects.get_or_create(name="developer")[0],
                    "document":"michael",
                    "user":get_user_model().objects.get_or_create(username="test")[0]
                }
            )[0],
            institution_branch=Branch.objects.get(code="95430"),
            identifier="12121212",
            overdraft_protection=False,
            overdraft_limit=250000,
            balance=0
        )

    def test_age(self):
        """
        To open a bank account, one must be older (or exactly) 16 years old.
        In this case, our client can't be younger than 16 years.
        """

        assert self.maria_account.birthday <= date.today()-timedelta(days=16*365)
        assert self.kyle_account.birthday <= date.today()-timedelta(days=16*365)

    def test_age_validators(self):
        """
        Let's check if the validators are working correctly to check if the client is older than 16 and/or older than 18
        """
        assert personUtils.check_16_older(self.kyle_account.birthday)
        assert personUtils.check_18_older(self.maria_account.birthday)
