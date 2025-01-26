from rest_framework import serializers
from django.core.serializers.json import Serializer
from apps.account.models import Account, AccountTransactionHistory, MoneyTransfer

class AccountSerializer(serializers.ModelSerializer):
    account_holder_name = serializers.CharField(source='account_holder.name', read_only=True)
    institution_branch_name = serializers.CharField(source='institution_branch.name', read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'account_holder_name',
            'institution_branch_name',
            'identifier',
            'last_login',
            'overdraft_protection',
            'overdraft_limit',
            'balance',
        ]

class BasicAccountSerializer(Serializer):
    account_holder_name = serializers.CharField(source='account_holder.name', read_only=True)
    institution_branch_name = serializers.CharField(source='institution_branch.name', read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'account_holder_name',
            'institution_branch_name',
            'identifier',
            'last_login',
            'overdraft_protection',
            'overdraft_limit',
            'balance',
        ]

class AccountTransactionHistorySerializer(Serializer):
    class Meta:
        model = AccountTransactionHistory
        fields = "__all__"

class MoneyTransferSerializer(Serializer):
    class Meta:
        model = MoneyTransfer
        fields = "__all__"

class MoneyTransferExpandedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyTransfer
        fields = "__all__"