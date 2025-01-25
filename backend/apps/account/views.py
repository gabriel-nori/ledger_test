from apps.account.serializers import (
    AccountSerializer,
    AccountTransactionHistorySerializer,
    MoneyTransferSerializer,
    MoneyTransferExpandedSerializer
)
from apps.account.models import Account, AccountTransactionHistory, MoneyTransfer
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.account.permissions import IsOwnerOrSuperuser
from rest_framework.permissions import IsAuthenticated
from apps.financial_institution.models import Branch
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
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
        """
        According to the modeling, a user can have more than one account.
        We need to get the specific account that the user wants to use
        """
        target_account = None
        source_account = None
        user = request.user

        if not set(
            (
                "source_account",
                "target_account",
                "ammount"
            )
        ).issubset(request.data.keys()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        source_account_id = request.data["source_account"]
        target_account_id = request.data["target_account"]
        ammount = request.data["ammount"]

        if ammount <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
        try:
            target_account = Account.objects.get(identifier=target_account_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            source_account = Account.objects.get(identifier=source_account_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if source_account.account_holder.user != user:
            return Response(status=status.HTTP_403_NOT_AUTHORIZED)
        
        try:
            services.create_transfer(source_account, target_account, ammount)
            return Response(status=status.HTTP_200_OK)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=["get"])
    def list_transfers_received(self, request, pk):
        transfers = MoneyTransfer.objects.filter(origin__id=pk)
        serializer = MoneyTransferSerializer()
        return HttpResponse(serializer.serialize(transfers))

    @action(detail=True, methods=["get"])
    def list_transfers_sent(self, request, pk):
        transfers = MoneyTransfer.objects.filter(destination__id=pk)
        serializer = MoneyTransferSerializer()
        return HttpResponse(serializer.serialize(transfers))
    
    @action(detail=True, methods=["get"])
    def list_history(self, request, pk):
        user = request.user
        history = AccountTransactionHistory.objects.filter(account__id=pk, account__account_holder__user=user)
        serializer = AccountTransactionHistorySerializer()
        return HttpResponse(serializer.serialize(history))
    
class MoneyTransferView(ReadOnlyModelViewSet):
    queryset = MoneyTransfer.objects.all()
    serializer_class = MoneyTransferExpandedSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["delete"])
    def cancel_transfer(self, request, pk):
        user = request.user
        transfer: MoneyTransfer = None
        try:
            transfer = MoneyTransfer.objects.get(transaction_id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not transfer.origin.account_holder.user == user:
            return Response(status=status.HTTP_403_NOT_AUTHORIZED)
        
        try:
            services.cancel_transaction(transfer)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)