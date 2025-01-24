from apps.financial_institution.models import Branch
from apps.person.models import Person
from django.db import models

class Account(models.Model):
    account_holder = models.ForeignKey(Person, on_delete=models.PROTECT)
    institution_branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    identifier = models.CharField(max_length=6)
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