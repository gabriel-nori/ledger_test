from apps.account.serializers import AccountSerializer, AccountCreateSerializer
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

class AccountListView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
    search_fields = ['account_holder__name', 'institution_branch__name']

class CreateAccountView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def create_account(self, request, pk=None):
        user = self.get_object()
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            branch = Branch.objects.get(id=serializer.validated_data['branch'])
            services.build_account(user, branch)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )