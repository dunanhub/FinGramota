from django.contrib import admin

from marketplace.models import (
    Bank,
    BankSourceMapping,
    CreditCardDetails,
    CreditDetails,
    DebitCardDetails,
    DepositDetails,
    MarketplaceProduct,
    MortgageDetails,
)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'official_url']
    search_fields = ['name']


@admin.register(BankSourceMapping)
class BankSourceMappingAdmin(admin.ModelAdmin):
    list_display = [
        'external_name',
        'external_alias',
        'bank',
        'source',
    ]
    list_filter = ['source']
    search_fields = [
        'external_name',
        'external_alias',
        'bank__name',
    ]
    autocomplete_fields = ['bank']


@admin.register(MarketplaceProduct)
class MarketplaceProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'bank',
        'category',
        'is_active',
        'source_updated_at',
        'scraped_at',
    ]
    list_filter = ['category', 'is_active', 'source']
    search_fields = ['name', 'bank__name', 'source_alias']
    autocomplete_fields = ['bank']
    readonly_fields = [
        'source_product_id',
        'source',
        'scraped_at',
        'last_seen_at',
        'raw_data',
    ]


admin.site.register(DepositDetails)
admin.site.register(CreditDetails)
admin.site.register(MortgageDetails)
admin.site.register(CreditCardDetails)
admin.site.register(DebitCardDetails)