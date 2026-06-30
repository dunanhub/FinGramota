from rest_framework import serializers

from verification.services import VerificationStatus


class VerificationSearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255, trim_whitespace=True)
    size = serializers.IntegerField(min_value=1, max_value=20, default=10, required=False)


class SourceSerializer(serializers.Serializer):
    api_uri = serializers.CharField()
    version = serializers.CharField()


class OrganizationSerializer(serializers.Serializer):
    bin = serializers.CharField(allow_null=True)
    name_ru = serializers.CharField(allow_null=True)
    name_kk = serializers.CharField(allow_null=True)
    director = serializers.CharField(allow_null=True)
    registration_date = serializers.DateField(allow_null=True)
    registration_date_source = serializers.CharField(allow_null=True)
    status_ru = serializers.CharField(allow_null=True)
    status_kk = serializers.CharField(allow_null=True)
    address_ru = serializers.CharField(allow_null=True)
    address_kk = serializers.CharField(allow_null=True)
    activity_ru = serializers.CharField(allow_null=True)
    activity_kk = serializers.CharField(allow_null=True)
    source_id = serializers.CharField(allow_null=True)
    source = SourceSerializer()


class LicenseSerializer(serializers.Serializer):
    organization_name_ru = serializers.CharField(allow_null=True)
    organization_name_kk = serializers.CharField(allow_null=True)
    license_number = serializers.CharField(allow_null=True)
    license_number_normalized = serializers.CharField(allow_null=True)
    issued_at = serializers.DateField(allow_null=True)
    issued_at_source = serializers.CharField(allow_null=True)
    address = serializers.CharField(allow_null=True)
    address_alt = serializers.CharField(allow_null=True)
    source_id = serializers.CharField(allow_null=True)
    source = SourceSerializer()


class VerificationResultSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=VerificationStatus.CHOICES)
    query = serializers.CharField()
    organizations = OrganizationSerializer(many=True)
    licenses = LicenseSerializer(many=True)
    message = serializers.CharField(allow_null=True)


class PyramidCheckResultSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=VerificationStatus.CHOICES)
    query = serializers.CharField()
    organizations = OrganizationSerializer(many=True)
    licenses = LicenseSerializer(many=True)
    message = serializers.CharField(allow_null=True)
    limitations = serializers.ListField(child=serializers.CharField())
