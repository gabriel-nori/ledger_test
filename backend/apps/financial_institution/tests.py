from apps.financial_institution.models import Branch, BranchClient, Institution, InstitutionType
from apps.location.models import Country, Street
from django.test import TestCase

class TestFinancialInstitution(TestCase):
    def setUp(self):
        institution_type = InstitutionType.objects.create(name="bank")

        alpha_bank = Institution.objects.create(
            name="Alpha Bank",
            type=institution_type,
            code="12409",
            country=Country.objects.get(name="Brazil")
        )

        not_a_bank = Institution.objects.create(
            name="Not a Bank",
            type=institution_type,
            code="09832",
            country=Country.objects.get(name="Brazil")
        )

        good_savings_bank = Institution.objects.create(
            name="Good Savings Bank",
            type=institution_type,
            code="95430",
            country=Country.objects.get(name="Argentina")
        )

        alpha_bank_01 = Branch.objects.create(
            institution=alpha_bank,
            street=Street.objects.get(name="Croata"),
            number=123,
            floor=None,
            room=None,
            code=None
        )

        not_a_bank_01 = Branch.objects.create(
            institution=not_a_bank,
            street=Street.objects.get(name="Croata"),
            number=201,
            floor=None,
            room=None,
            code=None
        )

        good_savings_bank_01 = Branch.objects.create(
            institution=good_savings_bank,
            street=Street.objects.get(name="Acasusso"),
            number=91,
            floor=None,
            room=None,
            code=None
        )