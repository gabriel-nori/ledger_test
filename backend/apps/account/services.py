from apps.financial_institution.models import Branch
from apps.person import utils as personUtils
from apps.account.models import Account
from apps.person.models import Person
import uuid

def generate_account_identifier() -> str:
    """
    This method generates a six digits number based on a UUID.
    Since this is just a proof of concept, the UUID4 is being used and
    its last part is stripped to get the account identifier
    """
    return (str(uuid.uuid4()).split("-")[4])[0:6]

def build_account(user: Person, branch: Branch) -> Account|None:
    """
    This method is the entry point to create a new bank account for the client.
    At this point, the client must have completed the registration.
    After inserting the user here, we need to generate a new account number based on bussiness logic.
    First, we need to check, again, just to play on the safe side, if the client is under 18 or 16. This is going to change from country to country.
    To simplify testing and development, I'm going to assume 18.
    """
    if not personUtils.check_18_older(user.birthday):
        return
    
    