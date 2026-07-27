from decimal import Decimal

from rest_framework import serializers

from marketplace.models import (
    Bank,
    CreditCardDetails,
    CreditDetails,
    DebitCardDetails,
    DepositDetails,
    MarketplaceProduct,
    MortgageDetails,
)


class NumericModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for name, value in representation.items():
            model_value = getattr(instance, name, None)
            if isinstance(model_value, Decimal) and value is not None:
                representation[name] = float(model_value)
        return representation


class BankSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Bank
        fields = ['name', 'slug', 'official_url']


class DepositDetailsSerializer(NumericModelSerializer):
    class Meta:
        model = DepositDetails
        exclude = ['id', 'product']


class CreditDetailsSerializer(NumericModelSerializer):
    class Meta:
        model = CreditDetails
        exclude = ['id', 'product']


class MortgageDetailsSerializer(NumericModelSerializer):
    class Meta:
        model = MortgageDetails
        exclude = ['id', 'product']


class CreditCardDetailsSerializer(NumericModelSerializer):
    class Meta:
        model = CreditCardDetails
        exclude = ['id', 'product']


class DebitCardDetailsSerializer(NumericModelSerializer):
    class Meta:
        model = DebitCardDetails
        exclude = ['id', 'product']


DETAIL_SERIALIZERS = {
    MarketplaceProduct.Category.DEPOSIT: (
        'deposit_details',
        DepositDetailsSerializer,
    ),
    MarketplaceProduct.Category.CREDIT: (
        'credit_details',
        CreditDetailsSerializer,
    ),
    MarketplaceProduct.Category.MORTGAGE: (
        'mortgage_details',
        MortgageDetailsSerializer,
    ),
    MarketplaceProduct.Category.CREDIT_CARD: (
        'credit_card_details',
        CreditCardDetailsSerializer,
    ),
    MarketplaceProduct.Category.DEBIT_CARD: (
        'debit_card_details',
        DebitCardDetailsSerializer,
    ),
}


class MarketplaceProductSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = MarketplaceProduct
        fields = [
            'id',
            'category',
            'name',
            'features',
            'details',
            'source_url',
            'source_updated_at',
            'scraped_at',
        ]

    def get_details(self, product):
        related_name, serializer_class = DETAIL_SERIALIZERS[product.category]
        details = getattr(product, related_name, None)
        if details is None:
            return {}
        return serializer_class(details).data


class MarketplaceProductListSerializer(MarketplaceProductSerializer):
    bank = BankSerializer(read_only=True)

    class Meta(MarketplaceProductSerializer.Meta):
        fields = [
            'id',
            'category',
            'name',
            'bank',
            'features',
            'details',
            'source_url',
            'source_updated_at',
            'scraped_at',
        ]


class BankDetailSerializer(BankSerializer):
    products = serializers.SerializerMethodField()

    class Meta(BankSerializer.Meta):
        fields = ['name', 'slug', 'official_url', 'products']

    def get_products(self, bank):
        grouped = {
            'deposits': [],
            'credits': [],
            'mortgages': [],
            'credit_cards': [],
            'debit_cards': [],
        }
        category_keys = {
            MarketplaceProduct.Category.DEPOSIT: 'deposits',
            MarketplaceProduct.Category.CREDIT: 'credits',
            MarketplaceProduct.Category.MORTGAGE: 'mortgages',
            MarketplaceProduct.Category.CREDIT_CARD: 'credit_cards',
            MarketplaceProduct.Category.DEBIT_CARD: 'debit_cards',
        }
        products = getattr(bank, 'active_products', [])
        for product in products:
            key = category_keys[product.category]
            grouped[key].append(MarketplaceProductSerializer(product).data)
        return grouped