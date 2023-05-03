from django.urls import path
from .views import LoginView, AuthenticatedView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('authenticated/', AuthenticatedView.as_view(), name='authenticated'),
]
