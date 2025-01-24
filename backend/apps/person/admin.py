from apps.person.models import (
    ActivityArea,
    Interest,
    Person,
    PersonInterest,
    PersonSocialNetwork,
    Prospect,
    ProspectDeclineReason,
    SocialNetwork
)
from django.contrib import admin

class PersonInterestAdmin(admin.ModelAdmin):
    list_display = [
        "get_person",
        "get_interest"
    ]

    def get_interest(self, obj):
        return obj.interest.name
    
    get_interest.short_description = "interest"
    get_interest.admin_order_field  = "interest"

    def get_person(self, obj):
        return obj.person.name
    
    get_person.short_description = "person"
    get_person.admin_order_field  = "person"

class PersonSocialNetworkAdmin(admin.ModelAdmin):
    list_display = [
        "get_person",
        "get_social_network",
        "profile_url"
    ]

    def get_person(self, obj):
        return obj.person.name
    
    get_person.short_description = "person"
    get_person.admin_order_field  = "person"

    def get_social_network(self, obj):
        return obj.social_network.name
    
    get_social_network.short_description = "social network"
    get_social_network.admin_order_field  = "social network"

class ProspectkAdmin(admin.ModelAdmin):
    list_display = [
        "get_person",
        "get_responsible",
        "contacted",
        "returned_contact",
        "meeting_scheduled",
        "declined"
    ]

    def get_person(self, obj):
        return obj.person.name
    
    get_person.short_description = "person"
    get_person.admin_order_field  = "person"

    def get_responsible(self, obj):
        return obj.responsible.username
    
    get_responsible.short_description = "responsible"
    get_responsible.admin_order_field  = "responsible"

class PersonAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sex",
        "primary_email",
        "get_area_of_activity"
    ]

    def get_area_of_activity(self, obj):
        return obj.area_of_activity.name
    
    get_area_of_activity.short_description = "area of activity"
    get_area_of_activity.admin_order_field  = "area of activity"

admin.site.register(ActivityArea)
admin.site.register(Interest)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonInterest, PersonInterestAdmin)
admin.site.register(PersonSocialNetwork, PersonSocialNetworkAdmin)
admin.site.register(Prospect, ProspectkAdmin)
admin.site.register(ProspectDeclineReason)
admin.site.register(SocialNetwork)