from apps.account.models import Account, AccountTransactionHistory, MoneyTransfer
from apps.financial_institution.models import Branch
from apps.person import utils as personUtils
from apps.person.models import Person
from apps.account import logger
import uuid


def generate_account_identifier() -> str:
    """
    This method generates a six digits number based on a UUID.
    Since this is just a proof of concept, the UUID4 is being used and
    its last part is stripped to get the account identifier
    """
    return (str(uuid.uuid4()).split("-")[4])[0:6]


def build_account(user: Person, branch: Branch, overdraft_protection: bool) -> Account:
    """
    This method is the entry point to create a new bank account for the client.
    At this point, the client must have completed the registration.
    After inserting the user here, we need to generate a new account number based on bussiness logic.
    """

    if not isinstance(user, Person):
        raise ValueError("The provided user argument isn't a user object")
    if not isinstance(branch, Branch):
        raise ValueError("The provided branch argument isn't a branch object")
    if not isinstance(overdraft_protection, bool):
        raise ValueError(
            "The provided overdraft_protection argument isn't a bool object"
        )

    return Account(
        account_holder=user,
        institution_branch=branch,
        identifier=generate_account_identifier(),
        overdraft_protection=overdraft_protection,
        overdraft_limit=10000,  # This should be replaced by a method to calculate the allowed ammount
        balance=0,
    )


def take_money(account: Account, ammount: int, refund: bool = False) -> bool:
    """
    This method receives the account object and the ammount to be taken in cents.
    if the ammount is less than what is available, it checks if overdraft is possible.
    """
    balance_before = account.balance
    if ammount <= 0:
        raise ValueError("The ammount provided is less than 0")
    if account.balance >= ammount:
        account.balance -= ammount
    elif account.overdraft_protection:
        raise ValueError("Value is above client balance")
    else:
        if account.overdraft_limit + account.balance > ammount:
            account.balance -= ammount
        else:
            raise ValueError("Value is above client overdraft limit")
    if account.balance == balance_before - ammount:
        account.save()
        if not refund:
            AccountTransactionHistory.objects.create(
                account=account, operation_type="I", ammount=ammount
            )
        else:
            AccountTransactionHistory.objects.create(
                account=account, operation_type="C", ammount=ammount
            )
        return True


def put_money(account: Account, ammount: int, refund: bool = False) -> bool:
    if ammount <= 0:
        raise ValueError("The ammount provided is less than 0")
    balance_before = account.balance
    account.balance += ammount
    if account.balance == balance_before + ammount:
        account.save()
        if not refund:
            AccountTransactionHistory.objects.create(
                account=account, operation_type="I", ammount=ammount
            )
        else:
            AccountTransactionHistory.objects.create(
                account=account, operation_type="C", ammount=ammount
            )
        return True
    else:
        raise ValueError("The ammount provided couldn't be added to the account")


def create_transfer(origin: Account, destination: Account, ammount: int):
    """
    To create a new money transfer we need to first check if the client can do so an then proceed to the transaction.
    If the money isn't credited, we need to rollback and restore the balance
    """
    try:
        take_money(origin, ammount)
        try:
            put_money(destination, ammount)
            MoneyTransfer.objects.create(
                origin=origin, destination=destination, ammount=ammount
            )
            return True
        except ValueError as v:
            logger.error(
                "Failed to credit money to account",
                extras={
                    "origin_account": origin.identifier,
                    "destination_account": destination.identifier,
                    "ammount": ammount,
                    "available_balance": origin.balance,
                },
            )
            # Rollback operation
            put_money(origin, ammount, refund=True)
            raise ValueError("Failed to insert money on destination")

    except ValueError as v:
        logger.error(
            "Failed to take money from account",
            extras={
                "origin_account": origin.identifier,
                "destination_account": destination.identifier,
                "ammount": ammount,
                "available_balance": origin.balance,
            },
        )
        raise ValueError("Insufficient funds available")


def cancel_transaction(transaction: MoneyTransfer):
    try:
        if transaction.status == "R":
            logger.error(
                "Transaction already reverted",
                extras={
                    "transaction_id": transaction.transaction_id,
                    "ammount": transaction.ammount,
                    "revert_from": transaction.destination,
                    "revert_to": transaction.origin,
                },
            )
            raise AttributeError("Status is reverted already")
        else:
            create_transfer(
                transaction.destination, transaction.origin, transaction.ammount
            )
    except:
        logger.error(
            "No transaction found with the provided ID",
            extras={"transaction_id": transaction.transaction_id},
        )
        raise ValueError("Object not found for this ID")
