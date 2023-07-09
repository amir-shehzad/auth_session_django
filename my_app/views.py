from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_learning_django.customSessionAuth import CustomSessionAuthenticationBackend


class LoginView(APIView):
    authentication_classes = [CustomSessionAuthenticationBackend]

    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful.'})
        return Response({'message': 'Invalid credentials.'})


class AuthenticatedView(APIView):
    authentication_classes = [CustomSessionAuthenticationBackend]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        data = {'message': 'You are authenticated'}
        return Response(data)


class ResetSessionsView(APIView):
    authentication_classes = []
    permission_classes = []

    def delete(self, request: Request) -> Response:
        sessions = Session.objects.all()
        sessions.delete()

        return Response({"message": "Successfully reset"})
