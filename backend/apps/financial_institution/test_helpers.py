from apps.location import test_helpers as locationHelpers
from apps.financial_institution.models import *

institution_type = InstitutionType(name="bank")

alpha_bank = Institution(
    name="Alpha Bank",
    type=institution_type,
    code="12409",
    country=locationHelpers.brazil
)

not_a_bank = Institution(
    name="Not a Bank",
    type=institution_type,
    code="09832",
    country=locationHelpers.brazil
)

good_savings_bank = Institution(
    name="Good Savings Bank",
    type=institution_type,
    code="95430",
    country=locationHelpers.argentina
)

alpha_bank_01 = Branch(
    institution=alpha_bank,
    street=locationHelpers.croata,
    number=123,
    floor=None,
    room=None,
    code=None
)

not_a_bank_01 = Branch(
    institution=not_a_bank,
    street=locationHelpers.croata,
    number=201,
    floor=None,
    room=None,
    code=None
)

good_savings_bank_01 = Branch(
    institution=good_savings_bank,
    street=locationHelpers.acassuso,
    number=91,
    floor=None,
    room=None,
    code=None
)