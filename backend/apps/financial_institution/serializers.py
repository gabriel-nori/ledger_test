from apps.financial_institution.models import Institution, Branch
from rest_framework import serializers


class InstitutionSerializer(serializers.ModelSerializer):
    institution_type = serializers.CharField(source="type.name", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = Institution
        fields = [
            "id",
            "name",
            "institution_type",
            "code",
            "country_name",
        ]


class BranchSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(source="institution.name", read_only=True)
    institution_id = serializers.CharField(source="institution.id", read_only=True)

    class Meta:
        model = Branch
        fields = [
            "institution_name",
            "institution_id",
            "code",
        ]
