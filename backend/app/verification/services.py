from verification.clients import DataEgovError
from verification.clients.data_egov import DataEgovClient
from verification.normalizers import (
    looks_like_domain,
    looks_like_license_number,
    normalize_bin,
    normalize_license_number,
    normalize_search_name,
    parse_source_date,
)


class VerificationStatus:
    LICENSE_CONFIRMED = 'LICENSE_CONFIRMED'
    FOUND_IN_REGISTRY = 'FOUND_IN_REGISTRY'
    NOT_FOUND = 'NOT_FOUND'
    INCONCLUSIVE = 'INCONCLUSIVE'
    SOURCE_UNAVAILABLE = 'SOURCE_UNAVAILABLE'

    CHOICES = [
        LICENSE_CONFIRMED,
        FOUND_IN_REGISTRY,
        NOT_FOUND,
        INCONCLUSIVE,
        SOURCE_UNAVAILABLE,
    ]


class Dataset:
    LEGAL_ENTITIES_API_URI = 'gbd_ul'
    LEGAL_ENTITIES_VERSION = 'v1'
    MFO_LICENSES_API_URI = 'opendata-api-uri487'
    MFO_LICENSES_VERSION = 'v142'


class VerificationSearchService:
    def __init__(self, client=None):
        self.client = client or DataEgovClient()

    def search_organizations(self, query, size=10):
        normalized_bin = normalize_bin(query)
        source = self._build_legal_entities_source(query, normalized_bin, size)

        records = self.client.get_dataset(
            Dataset.LEGAL_ENTITIES_API_URI,
            Dataset.LEGAL_ENTITIES_VERSION,
            source=source,
        )
        records = self._as_list(records)
        records = self._deduplicate(records, 'bin', 'nameru', 'director')

        return [self._normalize_organization(record) for record in records]

    def search_licenses(self, query, organization_names=None, size=10):
        searches = []
        if looks_like_license_number(query):
            searches.append(('number_of_license', normalize_license_number(query)))

        normalized_name = normalize_search_name(query)
        if normalized_name:
            searches.extend([
                ('name', normalized_name),
                ('name1', normalized_name),
            ])

        for name in organization_names or []:
            value = normalize_search_name(name)
            if value:
                searches.extend([
                    ('name', value),
                    ('name1', value),
                ])

        records = []
        seen_searches = set()
        for field, value in searches:
            key = (field, value)
            if key in seen_searches:
                continue
            seen_searches.add(key)

            source = self._build_match_source(field, value, size)
            result = self.client.get_dataset(
                Dataset.MFO_LICENSES_API_URI,
                Dataset.MFO_LICENSES_VERSION,
                source=source,
            )
            records.extend(self._as_list(result))

        records = self._deduplicate(records, 'number_of_license', 'name', 'name1')
        return [self._normalize_license(record) for record in records[:size]]

    def check_license(self, query, size=10):
        if looks_like_domain(query):
            return {
                'status': VerificationStatus.INCONCLUSIVE,
                'query': query,
                'organizations': [],
                'licenses': [],
                'message': 'Current data.egov.kz datasets do not contain website/domain fields.',
            }

        try:
            organizations = self.search_organizations(query, size=size)
            organization_names = [
                item['name_ru']
                for item in organizations
                if item.get('name_ru')
            ]
            licenses = self.search_licenses(query, organization_names=organization_names, size=size)
        except DataEgovError:
            return {
                'status': VerificationStatus.SOURCE_UNAVAILABLE,
                'query': query,
                'organizations': [],
                'licenses': [],
                'message': 'data.egov.kz is unavailable or returned an invalid response.',
            }

        if licenses:
            status = VerificationStatus.LICENSE_CONFIRMED
        elif organizations:
            status = VerificationStatus.FOUND_IN_REGISTRY
        else:
            status = VerificationStatus.NOT_FOUND

        return {
            'status': status,
            'query': query,
            'organizations': organizations,
            'licenses': licenses,
            'message': None,
        }

    def check_pyramid(self, query, size=10):
        result = self.check_license(query, size=size)
        result['status'] = VerificationStatus.INCONCLUSIVE
        result['message'] = (
            'Current data.egov.kz datasets can verify legal entity registration '
            'and MFO licenses, but do not provide a confirmed financial pyramid registry.'
        )
        result['limitations'] = [
            'No official financial pyramid dataset was found on data.egov.kz.',
            'A negative license/registry result is not proof that the project is safe.',
            'AFM/ARDFM sources should be integrated later for confirmed pyramid checks.',
        ]
        return result

    def _build_legal_entities_source(self, query, normalized_bin, size):
        if normalized_bin:
            return self._build_match_source('bin', normalized_bin, size)

        normalized_name = normalize_search_name(query)
        return {
            'size': size,
            'query': {
                'bool': {
                    'should': [
                        {'match': {'nameru': normalized_name}},
                        {'match': {'namekz': normalized_name}},
                        {'match': {'director': normalized_name}},
                    ],
                    'minimum_should_match': 1,
                }
            },
        }

    @staticmethod
    def _build_match_source(field, value, size):
        return {
            'size': size,
            'query': {
                'bool': {
                    'must': [
                        {'match': {field: value}},
                    ]
                }
            },
        }

    @staticmethod
    def _normalize_organization(record):
        return {
            'bin': record.get('bin'),
            'name_ru': record.get('nameru'),
            'name_kk': record.get('namekz'),
            'director': record.get('director'),
            'registration_date': parse_source_date(record.get('datereg')),
            'registration_date_source': record.get('datereg'),
            'status_ru': record.get('statusru'),
            'status_kk': record.get('statuskz'),
            'address_ru': record.get('addressru'),
            'address_kk': record.get('addresskz'),
            'activity_ru': record.get('okedru'),
            'activity_kk': record.get('okedkz'),
            'source_id': record.get('id'),
            'source': {
                'api_uri': Dataset.LEGAL_ENTITIES_API_URI,
                'version': Dataset.LEGAL_ENTITIES_VERSION,
            },
        }

    @staticmethod
    def _normalize_license(record):
        return {
            'organization_name_ru': record.get('name'),
            'organization_name_kk': record.get('name1'),
            'license_number': record.get('number_of_license'),
            'license_number_normalized': normalize_license_number(record.get('number_of_license')),
            'issued_at': parse_source_date(record.get('date_of_granting_license')),
            'issued_at_source': record.get('date_of_granting_license'),
            'address': record.get('address'),
            'address_alt': record.get('address1'),
            'source_id': record.get('id'),
            'source': {
                'api_uri': Dataset.MFO_LICENSES_API_URI,
                'version': Dataset.MFO_LICENSES_VERSION,
            },
        }

    @staticmethod
    def _as_list(value):
        if isinstance(value, list):
            return value
        if isinstance(value, dict) and isinstance(value.get('result'), list):
            return value['result']
        if isinstance(value, dict):
            return [value]
        return []

    @staticmethod
    def _deduplicate(records, *fields):
        unique = []
        seen = set()
        for record in records:
            key = tuple(record.get(field) for field in fields)
            if key in seen:
                continue
            seen.add(key)
            unique.append(record)
        return unique
