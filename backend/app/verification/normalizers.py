import re
from datetime import datetime, timedelta
from urllib.parse import urlparse


LEGAL_FORM_PATTERNS = [
    r'\b\u0442\u043e\u043e\b',
    r'\b\u0430\u043e\b',
    r'\b\u043e\u043e\b',
    r'\b\u0438\u043f\b',
    r'\b\u0436\u0448\u0441\b',
    r'\b\u0430\u049b\b',
    r'\b\u049b\u0431\b',
    r'\b\u043c\u0438\u043a\u0440\u043e\u0444\u0438\u043d\u0430\u043d\u0441\u043e\u0432\u0430\u044f \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f\b',
    r'\b\u043c\u0438\u043a\u0440\u043e\u049b\u0430\u0440\u0436\u044b \u04b1\u0439\u044b\u043c\u044b\b',
]


def normalize_bin(value):
    digits = re.sub(r'\D+', '', str(value or ''))
    if len(digits) == 12:
        return digits
    return None


def normalize_domain(value):
    text = str(value or '').strip().lower()
    if not text:
        return ''

    if '://' not in text:
        text = f'https://{text}'

    parsed = urlparse(text)
    host = parsed.netloc or parsed.path
    host = host.split('@')[-1].split(':')[0].strip('.')

    if host.startswith('www.'):
        host = host[4:]

    return host


def normalize_license_number(value):
    text = str(value or '').strip().upper()
    text = text.replace('\u2116', '')
    text = text.replace('N ', '')
    text = re.sub(r'\s+', '', text)
    return text


def normalize_name(value):
    text = str(value or '').strip().lower()
    text = text.replace('\u00ab', '"').replace('\u00bb', '"')
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = re.sub(r'[^\w\s.-]+', ' ', text, flags=re.UNICODE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize_search_name(value):
    text = normalize_name(value)
    for pattern in LEGAL_FORM_PATTERNS:
        text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()


def looks_like_domain(value):
    domain = normalize_domain(value)
    return bool(domain and '.' in domain and not normalize_bin(value))


def looks_like_license_number(value):
    text = normalize_license_number(value)
    return bool(re.search(r'\d', text) and ('.' in text or '-' in text or len(text) >= 6))


def parse_source_date(value):
    if value in (None, ''):
        return None

    text = str(value).strip()
    if re.fullmatch(r'\d{4,6}', text):
        try:
            return (datetime(1899, 12, 30) + timedelta(days=int(text))).date().isoformat()
        except (OverflowError, ValueError):
            return None

    formats = [
        '%Y-%m-%d',
        '%Y-%m-%d%z',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%SZ',
        '%d.%m.%Y',
    ]
    for date_format in formats:
        try:
            return datetime.strptime(text, date_format).date().isoformat()
        except ValueError:
            continue

    return None
