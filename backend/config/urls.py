from apps.financial_institution.views import InstitutionView, BranchView
from apps.person.views import SigninView, ClientView
from rest_framework.schemas import get_schema_view
from apps.account.views import AccountView, MoneyTransferView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Ledger API",
        default_version="v1",
        description="Ledger API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"api/account", AccountView)
router.register(r"api/client", ClientView, basename="client")
router.register(r"api/institution", InstitutionView, basename="institution")
router.register(r"api/branch", BranchView, basename="branch")
router.register(r"api/money_transfer", MoneyTransferView, basename="money_transfer")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="ledger-swagger-ui",
    ),
    path("api/", include("rest_framework.urls")),
    path("api/signin/", SigninView.as_view()),
    path("api/auth/", obtain_auth_token, name="auth"),
]

urlpatterns += router.urls
