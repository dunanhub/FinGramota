from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import AllowAny

from marketplace.models import Bank
from marketplace.serializers import BankSerializer


class BankListView(generics.ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [AllowAny]


class BankDetailView(generics.RetrieveAPIView):
    serializer_class = BankSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        requested_slug = self.kwargs['slug']
        for bank in Bank.objects.all():
            if bank.slug == requested_slug:
                return bank
        raise Http404
