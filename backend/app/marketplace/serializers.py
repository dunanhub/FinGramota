from rest_framework import serializers

from marketplace.models import Bank


class BankSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Bank
        fields = ['name', 'slug', 'official_url']
