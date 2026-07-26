from django.contrib import admin

from marketplace.models import Bank


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'official_url']
    search_fields = ['name']
