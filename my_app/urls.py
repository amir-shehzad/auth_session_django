from django.urls import path
from .views import LoginView, AuthenticatedView, ResetSessionsView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('authenticated/', AuthenticatedView.as_view(), name='authenticated'),
    path('reset_sessions/', ResetSessionsView.as_view(), name='authenticated'),

]
