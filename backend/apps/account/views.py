from apps.account.serializers import AccountSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from apps.account.models import Account

class AccountListView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [SearchFilter]
    search_fields = ['account_holder__name', 'institution_branch__name']