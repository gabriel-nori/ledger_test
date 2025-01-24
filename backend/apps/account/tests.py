from apps.account import test_helpers as accountHelper
from apps.account.test_helpers import TestObjects
from apps.account.models import MoneyTransfer
from apps.account import services
from django.test import TestCase
from datetime import date

class AccountTest(TestCase):
    def setUp(self):
        self.test_objects = TestObjects()
        self.test_objects.create()
    
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
        self.assertRaises(ValueError, services.take_money, self.test_objects.fernando_account, 98765)
        self.test_objects.fernando_account.balance=98765
        assert services.take_money(self.test_objects.fernando_account, 98765)
        self.test_objects.fernando_account.balance=12345
        self.test_objects.fernando_account.overdraft_protection=False
        assert services.take_money(self.test_objects.fernando_account, 12348)
        assert self.test_objects.fernando_account.balance == -3

    def test_put_money(self):
        self.test_objects.fernando_account.balance=0
        assert services.put_money(self.test_objects.fernando_account, 12345)
        assert self.test_objects.fernando_account.balance == 12345
        
        self.test_objects.fernando_account.balance=0
        self.assertRaises(ValueError, services.put_money, self.test_objects.fernando_account, -12345)
        # assert self.test_objects.fernando_account.balance == 12345

    def test_make_transaction(self):
        transfer_ammount = 1000
        self.test_objects.fernando_account.balance = 0
        self.test_objects.fernando_account.overdraft_protection = True
        self.test_objects.fernando_account.save()

        self.test_objects.maria_account.balance = transfer_ammount
        self.test_objects.maria_account.overdraft_protection = True
        self.test_objects.maria_account.save()
        self.assertRaises(ValueError, services.create_transfer, self.test_objects.fernando_account, self.test_objects.maria_account, transfer_ammount)
        services.create_transfer(self.test_objects.maria_account, self.test_objects.fernando_account, transfer_ammount)
        assert self.test_objects.maria_account.balance == 0
        assert self.test_objects.fernando_account.balance == transfer_ammount
        assert MoneyTransfer.objects.get(
            origin=self.test_objects.maria_account,
            destination=self.test_objects.fernando_account,
            ammount=transfer_ammount
        ).ammount == transfer_ammount
