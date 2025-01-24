from apps.account.models import Account
from django.db import models
import uuid

class MoneyTransfer(models.Model):
    origin = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transfer_origin")
    destination = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transfer_destination")
    ammount = models.BigIntegerField()
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now=True)