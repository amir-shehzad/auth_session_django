from datetime import timedelta, datetime
from typing import Optional, Tuple

import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class CustomSessionAuthenticationBackend(SessionAuthentication):
    """
    Custom session authentication backend that allows authentication via username and password,
    and also via session ID. If username and password are provided, it checks them against the database.
    If session ID is provided, it delegates authentication to the parent SessionAuthentication class.
    """
    MAX_LOGIN_ATTEMPTS = 3
    BLOCKED_MINUTES = 2

    def enforce_csrf(self, request: Request) -> None:
        """
        Disable CSRF enforcement for this authentication backend.
        """
        return

    def authenticate(self, request: Request) -> Optional[Tuple[User, None]]:
        """
        Authenticates the user via username and password or via session ID.
        Returns a tuple of (user, None) if authentication succeeds, or None if authentication fails.
        Raises an AuthenticationFailed exception if there are too many login attempts or if the user is blocked.
        """

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            # Check if the session ID is present in the request
            session_id = request.COOKIES.get(settings.SESSION_COOKIE_NAME) or \
                         request.GET.get(settings.SESSION_COOKIE_NAME)

            if session_id:
                # If the session ID is present, delegate authentication to SessionAuthentication
                return super().authenticate(request)

            # If neither username/password nor session ID is present, return None
            return None

        # Check if user is blocked from logging in
        blocked_until = request.session.get('blocked_until')
        if blocked_until:
            blocked_until = datetime.fromtimestamp(blocked_until)
            if blocked_until > datetime.now():
                raise AuthenticationFailed(
                    f'You are blocked from logging in till {self.convert_to_localtime(blocked_until)}')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # Check if the password is correct
        if not user.check_password(password):
            request.session.setdefault('login_attempts', 0)
            # Increment incorrect login attempts counter
            request.session['login_attempts'] += 1
            if request.session['login_attempts'] >= self.MAX_LOGIN_ATTEMPTS:
                # Block user from logging in for BLOCKED_MINUTES minutes
                blocked_until = timezone.now() + timedelta(minutes=self.BLOCKED_MINUTES)
                request.session['blocked_until'] = blocked_until.timestamp()
                raise AuthenticationFailed(f"Too many incorrect login attempts. You are blocked from logging "
                                           f"in till {self.convert_to_localtime(blocked_until)}")

            return None
        else:
            # Reset login attempts and timer if login succeeds
            request.session.pop('blocked_until', None)
            request.session.pop('login_attempts', None)

            return user, None

    @staticmethod
    def convert_to_localtime(utctime: datetime, fmt: str = "%Y-%m-%d %H:%M") -> Optional[str]:
        """
        Converts a UTC datetime object to the local timezone (Asia/Karachi).
        Returns the converted datetime as a string formatted according to the given format string.
        """
        if not utctime:
            return utctime

        utc = utctime.replace(tzinfo=pytz.UTC)
        local_tz = utc.astimezone(pytz.timezone('Asia/Karachi'))

        return local_tz.strftime(fmt)
