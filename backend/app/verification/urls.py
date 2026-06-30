from django.urls import path

from verification.views import HealthView, LicenseSearchView, PyramidSearchView

urlpatterns = [
    path("api/verification/health/", HealthView.as_view(), name="verification-health"),
    path("api/verification/licenses/search/", LicenseSearchView.as_view(), name="verification-license-search"),
    path("api/verification/pyramids/search/", PyramidSearchView.as_view(), name="verification-pyramid-search"),
]
