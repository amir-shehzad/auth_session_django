from django.contrib.auth import authenticate, login
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.views.decorators.csrf import csrf_protect, csrf_exempt


# from auth_learning_django.customSessionAuth import CustomSessionAuthenticationBackend, MAX_LOGIN_ATTEMPTS

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
    # authentication_classes = [CustomSessionAuthenticationBackend]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {'message': 'You are authenticated'}
        return Response(data)
