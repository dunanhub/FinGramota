from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from marketplace.models import Bank


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
            reverse('marketplace-bank-detail', kwargs={'slug': self.bank.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.bank.name)

    def test_unknown_bank_returns_not_found(self):
        response = self.client.get(
            reverse('marketplace-bank-detail', kwargs={'slug': 'unknown-bank'})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
