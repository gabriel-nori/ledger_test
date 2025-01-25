from apps.account.serializers import AccountSerializer
from apps.account.permissions import IsOwnerOrSuperuser
from rest_framework.permissions import IsAuthenticated
from apps.financial_institution.models import Branch
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.account.models import Account
from rest_framework import status
from apps.account import services

class AccountView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
    search_fields = ['account_holder__name', 'institution_branch__name']

    @action(detail=False, methods=["post"])
    def create_transaction(self, request):
        account_obj = None
        user = request.user
        user_account = Account.objects.filter(account_holder__user=user).first()
        ammount = request.data["ammount"]
        target_account = request.data["account"]
        if ammount <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            account_obj = Account.objects.get(identifier=target_account)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            services.create_transfer(user_account, account_obj, ammount)
            return Response(status=status.HTTP_200_OK)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)