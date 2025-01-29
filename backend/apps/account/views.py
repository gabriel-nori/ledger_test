from apps.account.serializers import (
    AccountSerializer,
    AccountTransactionHistorySerializer,
    MoneyTransferSerializer,
    MoneyTransferExpandedSerializer,
    BasicAccountSerializer,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from apps.account.models import Account, AccountTransactionHistory, MoneyTransfer
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.account.permissions import IsOwnerOrSuperuser
from rest_framework.permissions import IsAuthenticated
from apps.financial_institution.models import Branch
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.person.models import Person
from django.http import HttpResponse
from rest_framework import status
from apps.account import services
from apps.account import logger
from drf_yasg import openapi


class AccountView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
    search_fields = ["account_holder__name", "institution_branch__name"]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    http_method_names = ["get", "post", "put", "patch"]
    lookup_field = "identifier"
    lookup_url_kwarg = "identifier"

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_description="Creates a new account for specified user and person",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["data"],
            properties={
                "overdraft_protection": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "person_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "branch_code": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def create_new(self, request):
        user = request.user
        person = None
        branch = None

        if not (
            request.data["overdraft_protection"]
            and request.data["person_id"]
            and request.data["branch_code"]
        ):
            logger.error("Bad request during account creation", extras={**request})
            return Response(status=status.HTTP_400_BAD_REQUEST)

        overdraft_protection = request.data["overdraft_protection"]
        person_id = request.data["person_id"]
        branch_code = request.data["branch_code"]

        try:
            person = Person.objects.get(id=person_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if person.user != user:
            return Response(status=status.HTTP_403_NOT_AUTHORIZED)

        try:
            branch = Branch.objects.get(code=branch_code)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not isinstance(overdraft_protection, bool):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = BasicAccountSerializer()
            return HttpResponse(
                serializer.serialize(
                    [services.build_account(person, branch, overdraft_protection)]
                )
            )

        except Exception as e:
            logger.error("Failed to create account", extras={"exception": str(e)})
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_description="Creates a new TRANSACTION",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["data"],
            properties={
                "source_account": openapi.Schema(type=openapi.TYPE_INTEGER),
                "target_account": openapi.Schema(type=openapi.TYPE_INTEGER),
                "ammount": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    def create_transaction(self, request):
        """
        According to the modeling, a user can have more than one account.
        We need to get the specific account that the user wants to use
        """
        target_account = None
        source_account = None
        user = request.user

        if not set(("source_account", "target_account", "ammount")).issubset(
            request.data.keys()
        ):
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
            services.create_transfer(source_account.id, target_account.id, ammount)
            return Response(status=status.HTTP_200_OK)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def list_transfers_received(self, request, identifier):
        transfers = MoneyTransfer.objects.filter(origin__identifier=identifier)
        serializer = MoneyTransferSerializer()
        return HttpResponse(serializer.serialize(transfers))

    @action(detail=True, methods=["get"])
    def list_transfers_sent(self, request, identifier):
        transfers = MoneyTransfer.objects.filter(destination__identifier=identifier)
        serializer = MoneyTransferSerializer()
        return HttpResponse(serializer.serialize(transfers))

    @action(detail=True, methods=["get"])
    def list_history(self, request, identifier):
        user = request.user
        history = AccountTransactionHistory.objects.filter(
            account__identifier=identifier, account__account_holder__user=user
        )
        serializer = AccountTransactionHistorySerializer()
        return HttpResponse(serializer.serialize(history))

    @action(detail=True, methods=["post"])
    @swagger_auto_schema(
        operation_description="Creates a new TRANSACTION",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["data"],
            properties={
                "ammount": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    def put_money(self, request, identifier):
        """
        According to the modeling, a user can have more than one account.
        We need to get the specific account that the user wants to use
        """
        ammount = None
        user = request.user
        account = None

        if not (request.data["ammount"]):
            logger.error("No ammount provided", extras={"account_id": identifier})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ammount = request.data["ammount"]

        if not user.is_superuser:
            return Response(status=status.HTTP_403_NOT_AUTHORIZED)

        try:
            account = Account.objects.get(identifier=identifier)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            services.put_money(account, ammount)
            return Response(status=status.HTTP_200_OK)
        except ValueError as v:
            logger.error(
                "Couldn't add value to the account",
                extras={"account_identifier": identifier, "ammount": ammount},
            )


class MoneyTransferView(ReadOnlyModelViewSet):
    queryset = MoneyTransfer.objects.all()
    serializer_class = MoneyTransferExpandedSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

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
