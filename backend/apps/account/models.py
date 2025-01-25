from apps.financial_institution.models import Branch
from apps.person.models import Person
from django.db import models
import uuid

class Account(models.Model):
    account_holder = models.ForeignKey(Person, on_delete=models.PROTECT)
    institution_branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    identifier = models.CharField(max_length=6, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    overdraft_protection = models.BooleanField(default=True)
    overdraft_limit = models.BigIntegerField()
    balance = models.BigIntegerField()

    def __str__(self):
        return f"{self.institution_branch}-{self.identifier}"
    
class AccountTransactionHistory(models.Model):
    OPERATION_TYPES = [
        ("I", "Income"),
        ("O", "Outcome"),
        ("R", "Refund Income"),
        ("C", "Refund Outcome")
    ]
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    operation_type = models.CharField(choices=OPERATION_TYPES, max_length=1)
    ammount = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now=True)

class MoneyTransfer(models.Model):
    STATUS_OPTIONS = [("C", "Completed"), ("R", "Reverted")]
    origin = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transfer_origin")
    destination = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transfer_destination")
    ammount = models.BigIntegerField()
    transaction_id = models.UUIDField(default=uuid.uuid4)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, max_length=1, default="C")