from rest_framework import serializers
from apps.account.models import Account

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