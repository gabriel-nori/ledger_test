from apps.person.views import SigninView, ClientView
from rest_framework.schemas import get_schema_view
from apps.account.views import AccountListView, CreateAccountView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'api/account', AccountListView)
router.register(r'api/client', ClientView, basename='client')
router.register(r'api/new_account', CreateAccountView, basename='account_create')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include('rest_framework.urls')),
    path('api/signin/', SigninView.as_view())
]

urlpatterns += router.urls