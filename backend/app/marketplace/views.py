from django.db.models import Prefetch
from django.http import Http404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from marketplace.models import Bank, MarketplaceProduct
from marketplace.serializers import (
    BankDetailSerializer,
    BankSerializer,
    MarketplaceProductListSerializer,
)


PRODUCT_RELATED_FIELDS = [
    'bank',
    'deposit_details',
    'credit_details',
    'mortgage_details',
    'credit_card_details',
    'debit_card_details',
]


class BankListView(generics.ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [AllowAny]


class BankDetailView(generics.RetrieveAPIView):
    serializer_class = BankDetailSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        products = MarketplaceProduct.objects.filter(
            is_active=True,
        ).select_related(*PRODUCT_RELATED_FIELDS)

        queryset = Bank.objects.prefetch_related(
            Prefetch(
                'products',
                queryset=products,
                to_attr='active_products',
            )
        )

        requested_slug = self.kwargs['slug']
        for bank in queryset:
            if bank.slug == requested_slug:
                return bank
        raise Http404


class MarketplaceProductListView(generics.ListAPIView):
    serializer_class = MarketplaceProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = MarketplaceProduct.objects.filter(
            is_active=True,
        ).select_related(*PRODUCT_RELATED_FIELDS)

        category = self.request.query_params.get('category')
        if category:
            allowed = {value for value, _label in MarketplaceProduct.Category.choices}
            if category not in allowed:
                raise ValidationError({
                    'category': f'Allowed values: {", ".join(sorted(allowed))}.'
                })
            queryset = queryset.filter(category=category)

        bank_slug = self.request.query_params.get('bank')
        if bank_slug:
            bank = next(
                (item for item in Bank.objects.all() if item.slug == bank_slug),
                None,
            )
            if bank is None:
                raise ValidationError({'bank': 'Unknown bank slug.'})
            queryset = queryset.filter(bank=bank)

        return queryset