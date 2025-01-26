from apps.person.serializers import SiginSerializer, PersonSerializer, LoginSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.person.permissions import IsOwnerOrSuperuser
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
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

class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': [token.key], "Sucsses":"Login SucssesFully"}, status=status.HTTP_201_CREATED )
            return Response({'Massage': 'Invalid Username and Password'}, status=401)

class ClientView(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        # Superusers see all accounts, others only see their own
        if self.request.user.is_superuser:
            return Person.objects.all()
        return Person.objects.filter(user=self.request.user)