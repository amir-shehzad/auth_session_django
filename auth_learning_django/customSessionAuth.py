from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

MAX_LOGIN_ATTEMPTS = 5


class CustomSessionAuthenticationBackend(SessionAuthentication):
    def authenticate(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return None

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                request.session.setdefault('login_attempts', 0)
                request.session['login_attempts'] += 1
                if request.session['login_attempts'] >= MAX_LOGIN_ATTEMPTS:
                    # Block user from logging in for 10 minutes
                    request.session['blocked_until'] = timezone.now() + timedelta(minutes=10)
                    request.session['blocked_until'] = request.session['blocked_until'].timestamp()
                    raise AuthenticationFailed('Too many incorrect login attempts. Please try again later.')
            else:
                # Reset login attempts counter if login succeeds
                request.session.pop('login_attempts', None)

                # Check if user is blocked from logging in
                blocked_until = request.session.get('blocked_until')
                if blocked_until:
                    blocked_until = timezone.make_aware(datetime.fromtimestamp(blocked_until), pytz.timezone('UTC'))
                    if blocked_until > timezone.now():
                        raise AuthenticationFailed(f'You are blocked from logging in till {blocked_until}')
                    else:
                        request.session.pop('blocked_until', None)

                return user, None
        except User.DoesNotExist:
            return None