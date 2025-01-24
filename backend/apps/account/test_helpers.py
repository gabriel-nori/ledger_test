from apps.financial_institution import test_helpers as fiHelper
from apps.account.services import generate_account_identifier
from apps.person import test_helpers as personHelper
from apps.account.models import Account

kyle_account = Account(
    account_holder=personHelper.approved_client,
    institution_branch=fiHelper.not_a_bank_01,
    identifier=generate_account_identifier(),
    overdraft_protection=True,
    overdraft_limit=250000,
    balance=0
)

fernando_account = Account(
    account_holder=personHelper.fernando_ok,
    institution_branch=fiHelper.alpha_bank_01,
    identifier=generate_account_identifier(),
    overdraft_protection=True,
    overdraft_limit=250000,
    balance=0
)

maria_account = Account(
    account_holder=personHelper.maria_ok,
    institution_branch=fiHelper.good_savings_bank_01,
    identifier=generate_account_identifier(),
    overdraft_protection=False,
    overdraft_limit=250000,
    balance=0
)