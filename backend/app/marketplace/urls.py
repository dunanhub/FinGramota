from django.urls import path

from marketplace.views import BankDetailView, BankListView


urlpatterns = [
    path('api/marketplace/banks/', BankListView.as_view(), name='marketplace-bank-list'),
    path('api/marketplace/banks/<slug:slug>/', BankDetailView.as_view(), name='marketplace-bank-detail'),
]
