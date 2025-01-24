from apps.location.test_helpers import TestObjects as LocationObjects
from apps.financial_institution.models import *

class TestObjects():

    def create(self):
        self. location_objects = LocationObjects()
        self.location_objects.create()

        self.institution_type = InstitutionType.objects.get_or_create(name="bank")[0]

        self.alpha_bank = Institution.objects.get_or_create(
            name="Alpha Bank",
            type=self.institution_type,
            code="12409",
            country=self.location_objects.brazil
        )[0]

        self.not_a_bank = Institution.objects.get_or_create(
            name="Not a Bank",
            type=self.institution_type,
            code="09832",
            country=self.location_objects.brazil
        )[0]

        self.good_savings_bank = Institution.objects.get_or_create(
            name="Good Savings Bank",
            type=self.institution_type,
            code="95430",
            country=self.location_objects.argentina
        )[0]

        self.alpha_bank_01 = Branch.objects.get_or_create(
            institution=self.alpha_bank,
            street=self.location_objects.croata,
            number=123,
            floor=None,
            room=None,
            code="saar4"
        )[0]

        self.not_a_bank_01 = Branch.objects.get_or_create(
            institution=self.not_a_bank,
            street=self.location_objects.croata,
            number=201,
            floor=None,
            room=None,
            code="ssfg"
        )[0]

        self.good_savings_bank_01 = Branch.objects.get_or_create(
            institution=self.good_savings_bank,
            street=self.location_objects.acassuso,
            number=91,
            floor=None,
            room=None,
            code="xxfa"
        )[0]