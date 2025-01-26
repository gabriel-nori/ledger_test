from apps.location.models import (
    Continent,
    Country,
    State,
    County,
    City,
    Neighborhood,
    StreetType,
    Street,
)
from django.contrib import admin

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(County)
admin.site.register(City)
admin.site.register(Neighborhood)
admin.site.register(StreetType)
admin.site.register(Street)
