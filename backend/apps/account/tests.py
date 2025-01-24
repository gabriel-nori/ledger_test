from apps.account import test_helpers as accountHelper
from apps.account.models import Account
from django.test import SimpleTestCase
from apps.account import services

class AccountCreationTest(SimpleTestCase):
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
        assert accountHelper.fernando_account.balance == 12345