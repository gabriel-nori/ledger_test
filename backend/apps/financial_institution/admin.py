from apps.financial_institution.models import(
    InstitutionType,
    Institution,
    Branch,
    BranchClient
)
from django.contrib import admin

admin.site.register(InstitutionType)
admin.site.register(Institution)
admin.site.register(Branch)
admin.site.register(BranchClient)