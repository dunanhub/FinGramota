import uuid

import django.db.models.deletion
from django.db import migrations, models


VBR_BANK_MAPPINGS = [
    ('Alatau City Bank', '5aba116d-a103-4f76-8c22-345295244541', 'jusan-kz', 'Alatau City Bank'),
    ('Altyn Bank', '45441d00-8492-4c16-ba56-6b03fe91ac20', 'altyn-bank-kz', 'Алтын Банк (Altyn Bank KZ)'),
    ('Bank CenterCredit', '0eb9e028-47ae-49f8-963d-368e6dab3822', 'bcc-kz', 'Банк ЦентрКредит (Казахстан)'),
    ('Bank RBK', 'c5f5365a-b564-45af-b870-99f0f4d40d4e', 'rbk-kz', 'РБК Банк (RBK BANK)'),
    ('Bereke Bank', '8e66b7dd-329e-4ff5-90ea-a6c048666e24', 'sberbank-kz', 'Bereke Bank'),
    ('Eurasian Bank', 'd08ff0ad-9a2b-4a28-8e32-a4da645a31b5', 'eurasian-bank', 'Евразийский банк (Eurasian Bank)'),
    ('ForteBank', 'b2e70168-3c76-4af5-9c9a-dd42a85004d2', 'fortebank', 'Форте Банк (ForteBank KZ)'),
    ('Freedom Bank Kazakhstan', '2c8fcd60-a328-48b7-ba0d-515f86e11678', 'freedom-finance-bank', 'Фридом Финанс банк'),
    ('Halyk Bank', 'c47f49fc-6a6e-4f8f-8918-3316addb82f3', 'halyc-bank', 'Халык Банк (Народный банк Казахстана)'),
    ('Home Credit Bank', '4e057824-0d5a-4045-992c-c977cb8b8cda', 'hoym-kredit-kz', 'Хоум Кредит'),
    ('Kaspi Bank', 'e8400eab-2b76-4cbc-b1ca-647b271502a9', 'kaspi-bank-kz', 'Каспи Банк (Kaspi KZ)'),
    ('Kazakhstan-Ziraat International Bank', 'b081d3d4-dad1-47bd-98e1-b3b97a2da609', 'kzi-bank', 'КЗИ банк (KZI Bank)'),
    ('Nurbank', '2c425e8f-8053-4e4f-8880-ff65cd74a249', 'nurbank-kz', 'Нурбанк'),
    ('Otbasy Bank', 'fe71a58b-1d45-49da-bebb-9d374dff7390', 'otbasi-bank-kz', 'Отбасы банк'),
    ('VTB Bank Kazakhstan', '9dd04d0c-5537-4622-8517-da4959e8f874', 'vtb--kazahstan-', 'Банк ВТБ (Казахстан)'),
]


def seed_vbr_bank_mappings(apps, _schema_editor):
    Bank = apps.get_model('marketplace', 'Bank')
    BankSourceMapping = apps.get_model('marketplace', 'BankSourceMapping')
    for bank_name, external_id, external_alias, external_name in VBR_BANK_MAPPINGS:
        bank = Bank.objects.filter(name=bank_name).first()
        if bank is None:
            continue
        BankSourceMapping.objects.update_or_create(
            source='vbr',
            external_id=uuid.UUID(external_id),
            defaults={
                'bank': bank,
                'external_alias': external_alias,
                'external_name': external_name,
            },
        )


def remove_vbr_bank_mappings(apps, _schema_editor):
    BankSourceMapping = apps.get_model('marketplace', 'BankSourceMapping')
    BankSourceMapping.objects.filter(source='vbr').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('marketplace', '0002_seed_banks'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankSourceMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(default='vbr', max_length=50)),
                ('external_id', models.UUIDField()),
                ('external_alias', models.CharField(max_length=255)),
                ('external_name', models.CharField(max_length=255)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_mappings', to='marketplace.bank')),
            ],
            options={'ordering': ['source', 'external_name']},
        ),
        migrations.CreateModel(
            name='MarketplaceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('deposit', 'Deposit'), ('credit', 'Credit'), ('mortgage', 'Mortgage'), ('credit_card', 'Credit card'), ('debit_card', 'Debit card')], max_length=20)),
                ('source', models.CharField(default='vbr', max_length=50)),
                ('source_product_id', models.UUIDField()),
                ('source_alias', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=500)),
                ('source_url', models.URLField(max_length=1000)),
                ('features', models.JSONField(blank=True, default=list)),
                ('source_updated_at', models.DateTimeField(blank=True, null=True)),
                ('scraped_at', models.DateTimeField(auto_now=True)),
                ('last_seen_at', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('raw_data', models.JSONField(blank=True, default=dict)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='marketplace.bank')),
            ],
            options={'ordering': ['category', 'name']},
        ),
        migrations.CreateModel(
            name='DepositDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_min', models.BigIntegerField(blank=True, null=True)),
                ('amount_max', models.BigIntegerField(blank=True, null=True)),
                ('term_min_days', models.PositiveIntegerField(blank=True, null=True)),
                ('term_max_days', models.PositiveIntegerField(blank=True, null=True)),
                ('rate_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('rate_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('interest_payment', models.CharField(blank=True, max_length=255)),
                ('capitalization', models.BooleanField(default=False)),
                ('replenishment', models.BooleanField(default=False)),
                ('partial_withdrawal', models.BooleanField(default=False)),
                ('online_opening', models.BooleanField(default=False)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_details', to='marketplace.marketplaceproduct')),
            ],
        ),
        migrations.CreateModel(
            name='CreditDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_min', models.BigIntegerField(blank=True, null=True)),
                ('amount_max', models.BigIntegerField(blank=True, null=True)),
                ('term_min_months', models.PositiveIntegerField(blank=True, null=True)),
                ('term_max_months', models.PositiveIntegerField(blank=True, null=True)),
                ('rate_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('rate_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('gesv_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('gesv_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('purpose', models.CharField(blank=True, max_length=500)),
                ('income_proof_required', models.BooleanField(blank=True, null=True)),
                ('collateral', models.CharField(blank=True, max_length=500)),
                ('passport_only', models.BooleanField(default=False)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credit_details', to='marketplace.marketplaceproduct')),
            ],
        ),
        migrations.CreateModel(
            name='MortgageDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_min', models.BigIntegerField(blank=True, null=True)),
                ('amount_max', models.BigIntegerField(blank=True, null=True)),
                ('term_min_months', models.PositiveIntegerField(blank=True, null=True)),
                ('term_max_months', models.PositiveIntegerField(blank=True, null=True)),
                ('rate_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('rate_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('gesv_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('gesv_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('down_payment_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('down_payment_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('purpose', models.CharField(blank=True, max_length=500)),
                ('property_category', models.CharField(blank=True, max_length=500)),
                ('collateral', models.CharField(blank=True, max_length=500)),
                ('insurance_required', models.BooleanField(blank=True, null=True)),
                ('state_support', models.BooleanField(default=False)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mortgage_details', to='marketplace.marketplaceproduct')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit_min', models.BigIntegerField(blank=True, null=True)),
                ('limit_max', models.BigIntegerField(blank=True, null=True)),
                ('grace_period_min_days', models.PositiveIntegerField(blank=True, null=True)),
                ('grace_period_max_days', models.PositiveIntegerField(blank=True, null=True)),
                ('rate_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('rate_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('issuance_fee', models.BigIntegerField(blank=True, null=True)),
                ('service_fee', models.BigIntegerField(blank=True, null=True)),
                ('service_period', models.CharField(blank=True, max_length=100)),
                ('cashback_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('partner_cashback_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('payment_system', models.CharField(blank=True, max_length=100)),
                ('card_class', models.CharField(blank=True, max_length=100)),
                ('income_proof_required', models.BooleanField(blank=True, null=True)),
                ('installment', models.BooleanField(default=False)),
                ('free_notifications', models.BooleanField(default=False)),
                ('courier_delivery', models.BooleanField(default=False)),
                ('free_cash_withdrawal', models.BooleanField(default=False)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credit_card_details', to='marketplace.marketplaceproduct')),
            ],
        ),
        migrations.CreateModel(
            name='DebitCardDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_interest_min', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('balance_interest_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('issuance_fee', models.BigIntegerField(blank=True, null=True)),
                ('service_fee_first_year', models.BigIntegerField(blank=True, null=True)),
                ('service_fee_next_year', models.BigIntegerField(blank=True, null=True)),
                ('savings_account', models.BooleanField(blank=True, null=True)),
                ('cashback_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('partner_cashback_max', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('payment_system', models.CharField(blank=True, max_length=100)),
                ('card_class', models.CharField(blank=True, max_length=100)),
                ('free_notifications', models.BooleanField(default=False)),
                ('courier_delivery', models.BooleanField(default=False)),
                ('cash_withdrawal_tariffs', models.JSONField(blank=True, default=list)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='debit_card_details', to='marketplace.marketplaceproduct')),
            ],
        ),
        migrations.AddConstraint(
            model_name='banksourcemapping',
            constraint=models.UniqueConstraint(fields=('source', 'external_id'), name='unique_marketplace_source_external_id'),
        ),
        migrations.AddConstraint(
            model_name='banksourcemapping',
            constraint=models.UniqueConstraint(fields=('source', 'external_alias'), name='unique_marketplace_source_external_alias'),
        ),
        migrations.AddConstraint(
            model_name='marketplaceproduct',
            constraint=models.UniqueConstraint(fields=('source', 'source_product_id'), name='unique_marketplace_source_product'),
        ),
        migrations.AddIndex(
            model_name='marketplaceproduct',
            index=models.Index(fields=['bank', 'category', 'is_active'], name='market_bank_cat_active_idx'),
        ),
        migrations.RunPython(seed_vbr_bank_mappings, remove_vbr_bank_mappings),
    ]
