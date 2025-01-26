from apps.financial_institution.test_helpers import TestObjects
from django.test import TestCase


class TestFinancialInstitution(TestCase):
    def setUp(self):
        self.test_objects = TestObjects()
        self.test_objects.create()

    def test_branch_consistency(self):
        branch = self.test_objects.alpha_bank_01
        assert branch.code == "saar4"
        assert branch.institution.code == "12409"
