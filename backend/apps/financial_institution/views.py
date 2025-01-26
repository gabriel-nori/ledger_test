from apps.financial_institution.serializers import (
    InstitutionSerializer,
    BranchSerializer,
)
from apps.financial_institution.models import Institution, Branch
from rest_framework.viewsets import ReadOnlyModelViewSet


class InstitutionView(ReadOnlyModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class BranchView(ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
