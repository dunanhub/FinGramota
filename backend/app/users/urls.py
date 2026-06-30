from django.urls import path

from users.views import (
    ChangePasswordView,
    HealthView,
    LoginView,
    LogoutView,
    MeSettingsView,
    MeView,
    RefreshTokenView,
    RegisterView,
    UserSummaryView,
)

urlpatterns = [
    path("api/users/health/", HealthView.as_view(), name="users-health"),
    path("api/auth/register/", RegisterView.as_view(), name="auth-register"),
    path("api/auth/login/", LoginView.as_view(), name="auth-login"),
    path("api/auth/token/refresh/", RefreshTokenView.as_view(), name="auth-token-refresh"),
    path("api/auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("api/users/me/", MeView.as_view(), name="users-me"),
    path("api/users/me/settings/", MeSettingsView.as_view(), name="users-me-settings"),
    path("api/users/me/change-password/", ChangePasswordView.as_view(), name="users-me-change-password"),
    path("api/users/me/summary/", UserSummaryView.as_view(), name="users-me-summary"),
]
