from apps.financial_institution.models import InstitutionType, Institution, Branch
from django.contrib import admin

admin.site.register(InstitutionType)
admin.site.register(Institution)
admin.site.register(Branch)