from apps.account import test_helpers as accountHelper
from apps.financial_institution.models import Branch
from apps.person.models import Person, Occupation
from django.contrib.auth import get_user_model
from apps.account.models import Account
from apps.account import services
from django.test import TestCase
from datetime import date

class AccountTest(TestCase):
    def setUp(self):
        kyle_account = Account(
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
            identifier=services.generate_account_identifier(),
            overdraft_protection=True,
            overdraft_limit=250000,
            balance=0
        )

        fernando_account = Account(
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
            identifier=services.generate_account_identifier(),
            overdraft_protection=True,
            overdraft_limit=250000,
            balance=0
        )

        maria_account = Account(
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
            identifier=services.generate_account_identifier(),
            overdraft_protection=False,
            overdraft_limit=250000,
            balance=0
        )
    
    def test_identifier_generation(self):
        identifier_1 = services.generate_account_identifier()
        identifier_2 = services.generate_account_identifier()
        identifier_3 = services.generate_account_identifier()

        assert isinstance(identifier_1, str)
        assert isinstance(identifier_2, str)
        assert isinstance(identifier_3, str)

        assert len(identifier_1) == 6
        assert len(identifier_2) == 6
        assert len(identifier_3) == 6
        assert identifier_1 != identifier_2 != identifier_3
    
    def test_account_obj_creation(self):
        return
        # assert not services.build_account()
    
    def test_take_money(self):
        assert not services.take_money(accountHelper.fernando_account, 98765)
        accountHelper.fernando_account.balance=98765
        assert services.take_money(accountHelper.fernando_account, 98765)
        accountHelper.fernando_account.balance=12345
        accountHelper.fernando_account.overdraft_protection=False
        assert services.take_money(accountHelper.fernando_account, 12348)
        assert accountHelper.fernando_account.balance == -3

    def test_put_money(self):
        accountHelper.fernando_account.balance=0
        assert services.put_money(accountHelper.fernando_account, 12345)
        assert accountHelper.fernando_account.balance == 12345
        
        accountHelper.fernando_account.balance=0
        assert not services.put_money(accountHelper.fernando_account, -12345)
        # assert accountHelper.fernando_account.balance == 12345