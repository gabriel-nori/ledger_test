from apps.person.models import Person
from apps.account.models import Account
from apps.financial_institution.models import Branch

def generate_account_identifier():
    return 1

def create_account(user: Person, branch: Branch):
    """
    This method is the entry point to create a new bank account for the client.
    At this point, the client must have completed the registration.
    After inserting the user here, we need to generate a new account number based on bussiness logic
    """
    return 1