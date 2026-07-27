import uuid
from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from marketplace.models import (
    Bank,
    DepositDetails,
    MarketplaceProduct,
)


class BankSeedDataTests(APITestCase):
    def test_initial_banks_are_loaded(self):
        self.assertEqual(Bank.objects.count(), 18)
        self.assertTrue(Bank.objects.filter(name='Halyk Bank').exists())
        self.assertTrue(Bank.objects.filter(name='Kaspi Bank').exists())


class BankApiTests(APITestCase):
    def setUp(self):
        Bank.objects.all().delete()
        self.bank = Bank.objects.create(
            name='Test Bank',
            official_url='https://bank.example.com/',
        )

    def test_list_banks(self):
        response = self.client.get(reverse('marketplace-bank-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                'name': 'Test Bank',
                'slug': 'test-bank',
                'official_url': 'https://bank.example.com/',
            }
        ])

    def test_get_bank_by_slug(self):
        response = self.client.get(
            reverse(
                'marketplace-bank-detail',
                kwargs={'slug': self.bank.slug},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.bank.name)
        self.assertEqual(response.data['products']['deposits'], [])

    def test_unknown_bank_returns_not_found(self):
        response = self.client.get(
            reverse(
                'marketplace-bank-detail',
                kwargs={'slug': 'unknown-bank'},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MarketplaceProductApiTests(APITestCase):
    def setUp(self):
        Bank.objects.all().delete()
        self.bank = Bank.objects.create(
            name='Kaspi Bank',
            official_url='https://kaspi.kz/',
        )
        self.product = MarketplaceProduct.objects.create(
            bank=self.bank,
            category=MarketplaceProduct.Category.DEPOSIT,
            source='vbr',
            source_product_id=uuid.uuid4(),
            source_alias='kaspi-depozit',
            name='Kaspi Депозит',
            source_url='https://www.vbr.kz/example/',
            features=['Пополнение'],
            last_seen_at=timezone.now(),
        )
        DepositDetails.objects.create(
            product=self.product,
            amount_min=1000,
            term_min_days=367,
            term_max_days=367,
            rate_min=Decimal('15'),
            rate_max=Decimal('15'),
            replenishment=True,
        )

    def test_bank_detail_groups_products(self):
        response = self.client.get(
            reverse(
                'marketplace-bank-detail',
                kwargs={'slug': self.bank.slug},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        deposits = response.data['products']['deposits']
        self.assertEqual(len(deposits), 1)
        self.assertEqual(deposits[0]['name'], 'Kaspi Депозит')
        self.assertEqual(deposits[0]['details']['amount_min'], 1000)
        self.assertEqual(deposits[0]['details']['rate_max'], 15.0)

    def test_product_list_can_be_filtered_by_category(self):
        response = self.client.get(
            reverse('marketplace-product-list'),
            {'category': MarketplaceProduct.Category.DEPOSIT},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['bank']['slug'], 'kaspi-bank')

    def test_invalid_category_returns_bad_request(self):
        response = self.client.get(
            reverse('marketplace-product-list'),
            {'category': 'unknown'},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_products_are_not_returned(self):
        self.product.is_active = False
        self.product.save(update_fields=['is_active'])

        response = self.client.get(reverse('marketplace-product-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])