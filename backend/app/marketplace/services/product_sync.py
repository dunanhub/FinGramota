import json
from dataclasses import dataclass
from pathlib import Path

from django.db import transaction
from django.utils import timezone

from marketplace.models import (
    BankSourceMapping,
    CreditCardDetails,
    CreditDetails,
    DebitCardDetails,
    DepositDetails,
    MarketplaceProduct,
    MortgageDetails,
)
from marketplace.scraping.vbr_parser import parse_catalog


CATEGORY_MODELS = {
    MarketplaceProduct.Category.DEPOSIT: DepositDetails,
    MarketplaceProduct.Category.CREDIT: CreditDetails,
    MarketplaceProduct.Category.MORTGAGE: MortgageDetails,
    MarketplaceProduct.Category.CREDIT_CARD: CreditCardDetails,
    MarketplaceProduct.Category.DEBIT_CARD: DebitCardDetails,
}


@dataclass
class SyncResult:
    created: int = 0
    updated: int = 0
    skipped: int = 0
    deactivated: int = 0


class ProductSyncService:
    source = 'vbr'

    @transaction.atomic
    def sync_from_directory(self, input_directory):
        input_directory = Path(input_directory)
        manifest = self._load_manifest(input_directory)
        if not manifest.get('completed'):
            raise ValueError('VBR capture is incomplete.')

        detail_pages = self._load_detail_pages(input_directory, manifest)
        mappings = {
            str(item.external_id): item
            for item in BankSourceMapping.objects.filter(source=self.source).select_related('bank')
        }
        seen_ids = set()
        result = SyncResult()
        now = timezone.now()

        for catalog in manifest.get('catalogs', []):
            category = catalog['category']
            for relative_path in catalog.get('files', []):
                html = (input_directory / relative_path).read_text(encoding='utf-8')
                for parsed in parse_catalog(html, category, detail_pages):
                    mapping = mappings.get(str(parsed.external_bank_id))
                    if mapping is None:
                        result.skipped += 1
                        continue
                    product, created = MarketplaceProduct.objects.update_or_create(
                        source=self.source,
                        source_product_id=parsed.source_product_id,
                        defaults={
                            'bank': mapping.bank,
                            'category': parsed.category,
                            'source_alias': parsed.source_alias,
                            'name': parsed.name,
                            'source_url': parsed.source_url,
                            'features': parsed.features,
                            'source_updated_at': parsed.source_updated_at,
                            'last_seen_at': now,
                            'is_active': True,
                            'raw_data': {
                                'fields': parsed.fields,
                                'external_bank_alias': parsed.external_bank_alias,
                                'external_bank_name': parsed.external_bank_name,
                            },
                        },
                    )
                    details_model = CATEGORY_MODELS[parsed.category]
                    details_model.objects.update_or_create(
                        product=product,
                        defaults=parsed.details,
                    )
                    seen_ids.add(parsed.source_product_id)
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1

        if not seen_ids:
            raise ValueError('No mapped bank products were found; existing data was preserved.')

        stale = MarketplaceProduct.objects.filter(source=self.source, is_active=True).exclude(
            source_product_id__in=seen_ids
        )
        result.deactivated = stale.update(is_active=False)
        return result

    def _load_manifest(self, input_directory):
        manifest_path = input_directory / 'manifest.json'
        if not manifest_path.exists():
            raise ValueError(f'Manifest not found: {manifest_path}')
        return json.loads(manifest_path.read_text(encoding='utf-8'))

    def _load_detail_pages(self, input_directory, manifest):
        pages = {}
        for item in manifest.get('products', []):
            relative_path = item.get('detail_file')
            source_url = item.get('source_url')
            if not relative_path or not source_url:
                continue
            path = input_directory / relative_path
            if path.exists():
                pages[source_url] = path.read_text(encoding='utf-8')
        return pages
