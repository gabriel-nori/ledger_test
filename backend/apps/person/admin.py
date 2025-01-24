from apps.person.models import (
    Occupation,
    Person,
    AddressType,
    PersonAddress
)
from django.contrib import admin

admin.site.register(Occupation)
admin.site.register(Person)
admin.site.register(AddressType)
admin.site.register(PersonAddress)