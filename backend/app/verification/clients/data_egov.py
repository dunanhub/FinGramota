import json
from urllib.parse import quote

import requests
from django.conf import settings


class DataEgovError(Exception):
    pass


class DataEgovConfigurationError(DataEgovError):
    pass


class DataEgovUnavailableError(DataEgovError):
    pass


class DataEgovResponseError(DataEgovError):
    pass


class DataEgovClient:
    def __init__(self, base_url=None, api_key=None, timeout=None, session=None):
        self.base_url = (base_url or settings.DATA_EGOV_BASE_URL).rstrip('/')
        self.api_key = api_key if api_key is not None else settings.DATA_EGOV_API_KEY
        self.timeout = timeout if timeout is not None else settings.DATA_EGOV_TIMEOUT
        self.session = session or requests.Session()

    def get_dataset(self, api_uri, version, source=None, detailed=False):
        prefix = 'api/detailed' if detailed else 'api/v4'
        path = self._build_dataset_path(prefix, api_uri, version)
        return self._get(path, source=source)

    def get_mapping(self, api_uri, version=None):
        path = self._build_dataset_path('api/v4/mapping', api_uri, version)
        return self._get(path)

    def get_metadata(self, api_uri, version):
        path = self._build_dataset_path('meta', api_uri, version)
        return self._get(path)

    def get_detailed_metadata(self, api_uri, version):
        path = self._build_dataset_path('meta/detailed', api_uri, version)
        return self._get(path)

    def _get(self, path, source=None):
        if not self.api_key:
            raise DataEgovConfigurationError('DATA_EGOV_API_KEY is not configured.')

        params = {'apiKey': self.api_key}
        if source is not None:
            params['source'] = json.dumps(source, ensure_ascii=False, separators=(',', ':'))

        try:
            response = self.session.get(
                f'{self.base_url}/{path}',
                params=params,
                timeout=self.timeout,
            )
        except (requests.ConnectionError, requests.Timeout) as exc:
            raise DataEgovUnavailableError('data.egov.kz request failed.') from exc
        except requests.RequestException as exc:
            raise DataEgovError('Unexpected data.egov.kz client error.') from exc

        if not response.ok:
            raise DataEgovResponseError(
                f'data.egov.kz returned HTTP {response.status_code}.'
            )

        try:
            return response.json()
        except ValueError as exc:
            raise DataEgovResponseError('data.egov.kz returned invalid JSON.') from exc

    @staticmethod
    def _build_dataset_path(prefix, api_uri, version=None):
        safe_api_uri = quote(str(api_uri).strip('/'), safe='')
        if not safe_api_uri:
            raise ValueError('api_uri is required.')

        parts = [prefix.strip('/'), safe_api_uri]
        if version is not None:
            safe_version = quote(str(version).strip('/'), safe='')
            if not safe_version:
                raise ValueError('version cannot be empty.')
            parts.append(safe_version)
        return '/'.join(parts)
