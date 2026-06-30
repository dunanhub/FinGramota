from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from verification.serializers import (
    PyramidCheckResultSerializer,
    VerificationResultSerializer,
    VerificationSearchRequestSerializer,
)
from verification.services import VerificationSearchService


class HealthView(APIView):
    @extend_schema(responses={200: dict})
    def get(self, request):
        return Response({
            'status': 'ready',
            'service': 'verification',
        })


class LicenseSearchView(APIView):
    @extend_schema(
        request=VerificationSearchRequestSerializer,
        responses={200: VerificationResultSerializer},
        examples=[
            OpenApiExample(
                'License number',
                value={'query': '04.21.0001.M', 'size': 10},
                request_only=True,
            ),
            OpenApiExample(
                'Organization name',
                value={'query': 'Кредит Time', 'size': 10},
                request_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = VerificationSearchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = VerificationSearchService().check_license(
            serializer.validated_data['query'],
            size=serializer.validated_data.get('size', 10),
        )
        return Response(result)


class PyramidSearchView(APIView):
    @extend_schema(
        request=VerificationSearchRequestSerializer,
        responses={200: PyramidCheckResultSerializer},
        examples=[
            OpenApiExample(
                'Project name or founder',
                value={'query': 'Project name or founder full name', 'size': 10},
                request_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = VerificationSearchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = VerificationSearchService().check_pyramid(
            serializer.validated_data['query'],
            size=serializer.validated_data.get('size', 10),
        )
        return Response(result)
