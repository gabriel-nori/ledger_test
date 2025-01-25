from apps.account.models import Account, MoneyTransfer, AccountTransactionHistory
from django.contrib import admin

admin.site.register(Account)
admin.site.register(MoneyTransfer)
admin.site.register(AccountTransactionHistory)