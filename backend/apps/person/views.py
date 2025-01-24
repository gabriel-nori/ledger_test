from apps.person.serializers import SiginSerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework import permissions
from apps.person.models import Person


class SigninView(CreateAPIView):
    queryset = Person.objects.all()
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = SiginSerializer