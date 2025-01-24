from apps.person.models import Person
from django.db import models

class Account(models.Model):
    account_holder = models.ForeignKey(Person, on_delete=models.PROTECT)
    identifier = models.CharField(max_length=6)
    last_login = models.DateTimeField(auto_now=True)
    overdraft_protection = models.BooleanField(default=True)
    overdraft_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=14, decimal_places=2) # A trillion... 99...99 billions, in reality