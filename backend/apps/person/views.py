from apps.person.serializers import SiginSerializer, PersonSerializer
from rest_framework.permissions import IsAuthenticated
from apps.person.permissions import IsOwnerOrSuperuser
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions
from apps.person.models import Person
from rest_framework import status


class SigninView(CreateAPIView):
    queryset = Person.objects.all()
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = SiginSerializer

class ClientView(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Superusers see all accounts, others only see their own
        if self.request.user.is_superuser:
            return Person.objects.all()
        return Person.objects.filter(user=self.request.user)