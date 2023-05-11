from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_learning_django.customSessionAuth import CustomSessionAuthenticationBackend


class LoginView(APIView):
    authentication_classes = [CustomSessionAuthenticationBackend]

    def post(self, request):
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

    def get(self, request):
        data = {'message': 'You are authenticated'}
        return Response(data)
