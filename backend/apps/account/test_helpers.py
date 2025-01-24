from apps.financial_institution.test_helpers import TestObjects as FinancialObjects
from apps.person.test_helpers import TestObjects as PersonObjects
from apps.account.services import generate_account_identifier
from apps.account.models import Account

class TestObjects():
    kyle_account = None
    fernando_account = None
    maria_account = None

    def create(self):
        self.person_objects = PersonObjects()
        self.person_objects.create()
        self.financial_objects = FinancialObjects()
        self.financial_objects.create()

        self.kyle_account = Account.objects.get_or_create(
            account_holder=self.person_objects.michael_ok,
            institution_branch=self.financial_objects.not_a_bank_01,
            identifier=generate_account_identifier(),
            overdraft_protection=True,
            overdraft_limit=250000,
            balance=0
        )[0]

        self.fernando_account = Account.objects.get_or_create(
            account_holder=self.person_objects.fernando_ok,
            institution_branch=self.financial_objects.alpha_bank_01,
            identifier=generate_account_identifier(),
            overdraft_protection=True,
            overdraft_limit=250000,
            balance=0
        )[0]

        self.maria_account = Account.objects.get_or_create(
            account_holder=self.person_objects.maria_ok,
            institution_branch=self.financial_objects.good_savings_bank_01,
            identifier=generate_account_identifier(),
            overdraft_protection=False,
            overdraft_limit=250000,
            balance=0
        )[0]