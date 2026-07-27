from django.db import models
from django.utils.text import slugify


class Bank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    official_url = models.URLField(max_length=500)

    class Meta:
        ordering = ['name']

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name


class BankSourceMapping(models.Model):
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name='source_mappings',
    )
    source = models.CharField(max_length=50, default='vbr')
    external_id = models.UUIDField()
    external_alias = models.CharField(max_length=255)
    external_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['source', 'external_name']
        constraints = [
            models.UniqueConstraint(
                fields=['source', 'external_id'],
                name='unique_marketplace_source_external_id',
            ),
            models.UniqueConstraint(
                fields=['source', 'external_alias'],
                name='unique_marketplace_source_external_alias',
            ),
        ]

    def __str__(self):
        return f'{self.source}: {self.external_name} -> {self.bank.name}'


class MarketplaceProduct(models.Model):
    class Category(models.TextChoices):
        DEPOSIT = 'deposit', 'Deposit'
        CREDIT = 'credit', 'Credit'
        MORTGAGE = 'mortgage', 'Mortgage'
        CREDIT_CARD = 'credit_card', 'Credit card'
        DEBIT_CARD = 'debit_card', 'Debit card'

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name='products',
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    source = models.CharField(max_length=50, default='vbr')
    source_product_id = models.UUIDField()
    source_alias = models.CharField(max_length=255)
    name = models.CharField(max_length=500)
    source_url = models.URLField(max_length=1000)
    features = models.JSONField(default=list, blank=True)
    source_updated_at = models.DateTimeField(null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now=True)
    last_seen_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['category', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['source', 'source_product_id'],
                name='unique_marketplace_source_product',
            ),
        ]
        indexes = [
            models.Index(
                fields=['bank', 'category', 'is_active'],
                name='market_bank_cat_active_idx',
            ),
        ]

    def __str__(self):
        return f'{self.bank.name}: {self.name}'


class DepositDetails(models.Model):
    product = models.OneToOneField(
        MarketplaceProduct,
        on_delete=models.CASCADE,
        related_name='deposit_details',
    )
    amount_min = models.BigIntegerField(null=True, blank=True)
    amount_max = models.BigIntegerField(null=True, blank=True)
    term_min_days = models.PositiveIntegerField(null=True, blank=True)
    term_max_days = models.PositiveIntegerField(null=True, blank=True)
    rate_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    rate_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    interest_payment = models.CharField(max_length=255, blank=True)
    capitalization = models.BooleanField(default=False)
    replenishment = models.BooleanField(default=False)
    partial_withdrawal = models.BooleanField(default=False)
    online_opening = models.BooleanField(default=False)


class CreditDetails(models.Model):
    product = models.OneToOneField(
        MarketplaceProduct,
        on_delete=models.CASCADE,
        related_name='credit_details',
    )
    amount_min = models.BigIntegerField(null=True, blank=True)
    amount_max = models.BigIntegerField(null=True, blank=True)
    term_min_months = models.PositiveIntegerField(null=True, blank=True)
    term_max_months = models.PositiveIntegerField(null=True, blank=True)
    rate_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    rate_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    gesv_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    gesv_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    purpose = models.CharField(max_length=500, blank=True)
    income_proof_required = models.BooleanField(null=True, blank=True)
    collateral = models.CharField(max_length=500, blank=True)
    passport_only = models.BooleanField(default=False)


class MortgageDetails(models.Model):
    product = models.OneToOneField(
        MarketplaceProduct,
        on_delete=models.CASCADE,
        related_name='mortgage_details',
    )
    amount_min = models.BigIntegerField(null=True, blank=True)
    amount_max = models.BigIntegerField(null=True, blank=True)
    term_min_months = models.PositiveIntegerField(null=True, blank=True)
    term_max_months = models.PositiveIntegerField(null=True, blank=True)
    rate_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    rate_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    gesv_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    gesv_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    down_payment_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    down_payment_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    purpose = models.CharField(max_length=500, blank=True)
    property_category = models.CharField(max_length=500, blank=True)
    collateral = models.CharField(max_length=500, blank=True)
    insurance_required = models.BooleanField(null=True, blank=True)
    state_support = models.BooleanField(default=False)


class CreditCardDetails(models.Model):
    product = models.OneToOneField(
        MarketplaceProduct,
        on_delete=models.CASCADE,
        related_name='credit_card_details',
    )
    limit_min = models.BigIntegerField(null=True, blank=True)
    limit_max = models.BigIntegerField(null=True, blank=True)
    grace_period_min_days = models.PositiveIntegerField(null=True, blank=True)
    grace_period_max_days = models.PositiveIntegerField(null=True, blank=True)
    rate_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    rate_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    issuance_fee = models.BigIntegerField(null=True, blank=True)
    service_fee = models.BigIntegerField(null=True, blank=True)
    service_period = models.CharField(max_length=100, blank=True)
    cashback_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    partner_cashback_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    payment_system = models.CharField(max_length=100, blank=True)
    card_class = models.CharField(max_length=100, blank=True)
    income_proof_required = models.BooleanField(null=True, blank=True)
    installment = models.BooleanField(default=False)
    free_notifications = models.BooleanField(default=False)
    courier_delivery = models.BooleanField(default=False)
    free_cash_withdrawal = models.BooleanField(default=False)


class DebitCardDetails(models.Model):
    product = models.OneToOneField(
        MarketplaceProduct,
        on_delete=models.CASCADE,
        related_name='debit_card_details',
    )
    balance_interest_min = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    balance_interest_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    issuance_fee = models.BigIntegerField(null=True, blank=True)
    service_fee_first_year = models.BigIntegerField(null=True, blank=True)
    service_fee_next_year = models.BigIntegerField(null=True, blank=True)
    savings_account = models.BooleanField(null=True, blank=True)
    cashback_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    partner_cashback_max = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    payment_system = models.CharField(max_length=100, blank=True)
    card_class = models.CharField(max_length=100, blank=True)
    free_notifications = models.BooleanField(default=False)
    courier_delivery = models.BooleanField(default=False)
    cash_withdrawal_tariffs = models.JSONField(default=list, blank=True)