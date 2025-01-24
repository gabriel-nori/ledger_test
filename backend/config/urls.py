from apps.person.views import SigninView, ClientView
from rest_framework.schemas import get_schema_view
from apps.account.views import AccountListView
from django.urls import include, path
from rest_framework import routers
from django.contrib import admin

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "api/specs/",
        get_schema_view(
            title="Ledger API specification",
            description="API specification",
            version="1.0.0"
        ),
        name="openapi-schema",
    ),
    path('api/', include('rest_framework.urls')),
    path('api/signin/', SigninView.as_view())
]


router.register(r'api/account/', AccountListView)
router.register(r'api/client/', ClientView)

urlpatterns += router.urls