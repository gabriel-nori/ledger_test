from apps.account import test_helpers as accountHelper
from apps.account.test_helpers import TestObjects
from apps.account.models import MoneyTransfer
from django.db.utils import OperationalError
from apps.account import services
from django.test import TestCase, TransactionTestCase
from datetime import date
import threading


class AccountTest(TransactionTestCase):
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
        with self.assertRaises(ValueError) as cm:
            services.build_account(None, None, False)
        exception = cm.exception
        assert str(exception) == "The provided user argument isn't a user object"

        with self.assertRaises(ValueError) as cm:
            services.build_account(
                self.test_objects.person_objects.fernando_ok, None, False
            )
        exception = cm.exception
        assert str(exception) == "The provided branch argument isn't a branch object"

        with self.assertRaises(ValueError) as cm:
            services.build_account(
                self.test_objects.person_objects.fernando_ok,
                self.test_objects.financial_objects.alpha_bank_01,
                "wrong_object",
            )
        exception = cm.exception
        assert (
            str(exception)
            == "The provided overdraft_protection argument isn't a bool object"
        )

        account = services.build_account(
            self.test_objects.person_objects.fernando_ok,
            self.test_objects.financial_objects.alpha_bank_01,
            True,
        )
        assert account.account_holder.name.lower() == "fernando"
        assert account.overdraft_protection == True
        assert account.balance == 0
        assert account.overdraft_limit == 10000
        assert len(account.identifier) == 6

    def test_take_money(self):
        self.assertRaises(
            ValueError, services.take_money, self.test_objects.fernando_account.id, 98765
        )
        self.test_objects.fernando_account.balance = 98765
        self.test_objects.fernando_account.save()
        assert services.take_money(self.test_objects.fernando_account.id, 98765)
        self.test_objects.fernando_account.balance = 12345
        self.test_objects.fernando_account.overdraft_protection = False
        self.test_objects.fernando_account.save()
        assert services.take_money(self.test_objects.fernando_account.id, 12348)
        self.test_objects.fernando_account.refresh_from_db()
        assert self.test_objects.fernando_account.balance == -3

    def test_put_money(self):
        self.test_objects.fernando_account.balance = 0
        self.test_objects.fernando_account.save()
        services.put_money(self.test_objects.fernando_account.id, 12345)
        self.test_objects.fernando_account.refresh_from_db()
        assert self.test_objects.fernando_account.balance == 12345

        self.test_objects.fernando_account.balance = 0
        self.test_objects.fernando_account.save()
        self.assertRaises(
            ValueError, services.put_money, self.test_objects.fernando_account.id, -12345
        )
        # assert self.test_objects.fernando_account.balance == 12345

    def test_make_transaction(self):
        transfer_ammount = 1000
        self.test_objects.fernando_account.balance = 0
        self.test_objects.fernando_account.overdraft_protection = True
        self.test_objects.fernando_account.save()

        self.test_objects.maria_account.balance = transfer_ammount
        self.test_objects.maria_account.overdraft_protection = True
        self.test_objects.maria_account.save()

        self.assertRaises(
            ValueError,
            services.create_transfer,
            self.test_objects.fernando_account.id,
            self.test_objects.maria_account.id,
            transfer_ammount,
        )
        services.create_transfer(
            self.test_objects.maria_account.id,
            self.test_objects.fernando_account.id,
            transfer_ammount,
        )
        self.test_objects.maria_account.refresh_from_db()
        self.test_objects.fernando_account.refresh_from_db()

        assert self.test_objects.maria_account.balance == 0
        assert self.test_objects.fernando_account.balance == transfer_ammount
        assert (
            MoneyTransfer.objects.get(
                origin=self.test_objects.maria_account,
                destination=self.test_objects.fernando_account,
                ammount=transfer_ammount,
            ).ammount
            == transfer_ammount
        )

    def test_transfer_revert(self):
        transfer_ammount = 1000
        self.test_objects.fernando_account.balance = 0
        self.test_objects.fernando_account.overdraft_protection = True
        self.test_objects.fernando_account.save()

        self.test_objects.maria_account.balance = transfer_ammount
        self.test_objects.maria_account.overdraft_protection = True
        self.test_objects.maria_account.save()
        services.create_transfer(
            self.test_objects.maria_account.id,
            self.test_objects.fernando_account.id,
            transfer_ammount,
        )

        self.test_objects.maria_account.refresh_from_db()
        self.test_objects.fernando_account.refresh_from_db()
        assert self.test_objects.maria_account.balance == 0
        assert self.test_objects.fernando_account.balance == transfer_ammount

        transaction = MoneyTransfer.objects.get(
            origin=self.test_objects.maria_account,
            destination=self.test_objects.fernando_account,
            ammount=transfer_ammount,
        )

        services.cancel_transaction(transaction)
        # assert self.test_objects.maria_account.balance == transfer_ammount
        # assert self.test_objects.fernando_account.balance == 0


    def test_multiple_requests_at_once(self):
        """
        This is a tricky test, but it is needed to ensure that the values are transfered correctly even if the method is called
        twice in the same time window.
        Since the test is using SQLite, we can have some lock problems during the test
        """
        ammount_to_be_taken = 1000
        self.test_objects.maria_account.balance = ammount_to_be_taken
        self.test_objects.maria_account.overdraft_limit = ammount_to_be_taken
        self.test_objects.maria_account.overdraft_protection = False
        self.test_objects.maria_account.save()

        self.test_objects.fernando_account.balance = 0
        self.test_objects.fernando_account.save()

        maria1 = threading.Thread(target=services.take_money, args=(self.test_objects.maria_account.id, 1000))
        maria2 = threading.Thread(target=services.take_money, args=(self.test_objects.maria_account.id, 1000))

        maria1.start()
        maria2.start()

        maria1.join()
        maria2.join()

        self.test_objects.maria_account.refresh_from_db()
        assert self.test_objects.maria_account.balance == -ammount_to_be_taken