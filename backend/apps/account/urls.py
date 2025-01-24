from apps.account.views import AccountListView
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'/', AccountListView)