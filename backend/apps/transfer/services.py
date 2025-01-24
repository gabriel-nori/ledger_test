from apps.account.models import Account, AccountTransactionHistory
from apps.account import services as accountServices
from apps.transfer.models import MoneyTransfer

def make_transfer(source: Account, destination: Account, ammount: int):
    if not accountServices.take_money(source):
        return
    if not accountServices.put_money(destination):
        return
    MoneyTransfer.objects.create(
        origin=source,
        destination=destination,
        ammount=ammount
    )

def cancel_transfer(uuid: str):
    try:
        transaction = MoneyTransfer.objects.get(transaction_id=uuid)
        if not accountServices.take_money(transaction.destination, transaction.ammount):
            return False
        accountServices.put_money(transaction.origin, transaction.ammount)
    except:
        raise "notFound"