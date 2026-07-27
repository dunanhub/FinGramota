import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from bs4 import BeautifulSoup
from django.utils import timezone


SPACE_RE = re.compile(r'\s+')
NUMBER_RE = re.compile(r'\d+(?:[\s\u00a0]\d{3})*(?:[,.]\d+)?')
UPDATED_RE = re.compile(r'Дата обновления:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2})?')


@dataclass(frozen=True)
class ParsedProduct:
    source_product_id: uuid.UUID
    source_alias: str
    name: str
    source_url: str
    external_bank_id: uuid.UUID
    external_bank_alias: str
    external_bank_name: str
    category: str
    features: list[str]
    source_updated_at: datetime | None
    fields: dict[str, str]
    details: dict


def clean_text(value):
    return SPACE_RE.sub(' ', value or '').strip()


def parse_catalog(html, category, detail_pages=None):
    soup = BeautifulSoup(html, 'html.parser')
    detail_pages = detail_pages or {}
    products = []
    for card in soup.select('.product-card-item[data-product-id][data-organization-id]'):
        parsed = parse_product_card(card, category, detail_pages)
        if parsed is not None:
            products.append(parsed)
    return products


def parse_product_card(card, category, detail_pages):
    title_link = card.select_one('.product-card-title-link[href]')
    if title_link is None:
        return None
    try:
        product_id = uuid.UUID(card.get('data-product-id', ''))
        bank_id = uuid.UUID(card.get('data-organization-id', ''))
    except ValueError:
        return None

    source_url = title_link.get('href', '').strip()
    fields = {}
    for column in card.select('.product-card-col'):
        title = column.select_one('.product-card-col-title')
        value = column.select_one('.product-card-col-text')
        if title is None or value is None:
            continue
        fields[clean_text(title.get_text(' ', strip=True))] = clean_text(
            value.get_text(' ', strip=True)
        )

    features = []
    for item in card.select('.product-card-advant-item'):
        value = clean_text(item.get_text(' ', strip=True))
        if value and value not in {'Ещё', 'Подробнее'} and value not in features:
            features.append(value)

    detail_html = detail_pages.get(source_url)
    source_updated_at = None
    detail_text = ''
    if detail_html:
        detail_soup = BeautifulSoup(detail_html, 'html.parser')
        detail_text = clean_text(detail_soup.get_text(' ', strip=True))
        source_updated_at = parse_updated_at(detail_text)

    details = build_category_details(category, fields, features, detail_text)
    return ParsedProduct(
        source_product_id=product_id,
        source_alias=card.get('data-product-alias', '').strip(),
        name=clean_text(title_link.get_text(' ', strip=True)),
        source_url=source_url,
        external_bank_id=bank_id,
        external_bank_alias=card.get('data-organization-alias', '').strip(),
        external_bank_name=clean_text(card.get('data-organization-name', '')),
        category=category,
        features=features,
        source_updated_at=source_updated_at,
        fields=fields,
        details=details,
    )


def parse_updated_at(text):
    match = UPDATED_RE.search(text)
    if not match:
        return None
    value = f'{match.group(1)} {match.group(2) or "00:00"}'
    parsed = datetime.strptime(value, '%d.%m.%Y %H:%M')
    return timezone.make_aware(parsed, timezone.get_current_timezone())


def parse_numeric_values(text):
    values = []
    for match in NUMBER_RE.finditer(text or ''):
        raw = match.group(0).replace(' ', '').replace('\u00a0', '').replace(',', '.')
        value = Decimal(raw)
        suffix = clean_text((text or '')[match.end():match.end() + 10]).lower()
        if suffix.startswith('млрд'):
            value *= Decimal('1000000000')
        elif suffix.startswith('млн'):
            value *= Decimal('1000000')
        elif suffix.startswith('тыс'):
            value *= Decimal('1000')
        values.append(value)
    return values


def parse_range(text, *, money=False):
    lowered = clean_text(text).lower()
    if not lowered or 'индивидуально' in lowered or 'любая' in lowered or lowered == 'нет':
        return None, None
    values = parse_numeric_values(text)
    if not values:
        return None, None
    if money:
        values = [value.quantize(Decimal('1')) for value in values]
    if len(values) >= 2:
        return values[0], values[-1]
    value = values[0]
    if lowered.startswith('до') or ' до ' in f' {lowered} ':
        return None, value
    if lowered.startswith('от'):
        return value, None
    return value, value


def parse_term_range(text, target_unit):
    matches = re.findall(
        r'(\d+(?:[,.]\d+)?)\s*(дн(?:я|ей)?|день|дней|мес(?:\.|яцев)?|год(?:а)?|лет)',
        clean_text(text).lower(),
    )
    if not matches:
        return None, None
    values = []
    for raw_value, unit in matches:
        value = Decimal(raw_value.replace(',', '.'))
        if target_unit == 'days':
            if unit.startswith('мес'):
                value *= 30
            elif unit.startswith('год') or unit == 'лет':
                value *= 365
        else:
            if unit.startswith('д'):
                value = max(Decimal('1'), value / 30)
            elif unit.startswith('год') or unit == 'лет':
                value *= 12
        values.append(int(value))
    lowered = clean_text(text).lower()
    if len(values) >= 2:
        return values[0], values[-1]
    if lowered.startswith('до'):
        return None, values[0]
    if lowered.startswith('от'):
        return values[0], None
    return values[0], values[0]


def field_value(fields, *names):
    for name in names:
        for title, value in fields.items():
            if name.lower() in title.lower():
                return value
    return ''


def has_feature(features, text):
    return any(text.lower() in feature.lower() for feature in features)


def build_category_details(category, fields, features, detail_text):
    builders = {
        'deposit': build_deposit_details,
        'credit': build_credit_details,
        'mortgage': build_mortgage_details,
        'credit_card': build_credit_card_details,
        'debit_card': build_debit_card_details,
    }
    return builders[category](fields, features, detail_text)


def build_deposit_details(fields, features, _detail_text):
    amount_min, amount_max = parse_range(field_value(fields, 'Сумма'), money=True)
    term_min, term_max = parse_term_range(field_value(fields, 'Срок'), 'days')
    rate_min, rate_max = parse_range(field_value(fields, 'Ставка'))
    payment = next(
        (feature for feature in features if 'выплата процентов' in feature.lower()),
        '',
    )
    return {
        'amount_min': amount_min,
        'amount_max': amount_max,
        'term_min_days': term_min,
        'term_max_days': term_max,
        'rate_min': rate_min,
        'rate_max': rate_max,
        'interest_payment': payment,
        'capitalization': has_feature(features, 'Капитализация'),
        'replenishment': has_feature(features, 'Пополнение'),
        'partial_withdrawal': has_feature(features, 'Частичное снятие'),
        'online_opening': has_feature(features, 'Открытие онлайн'),
    }


def build_credit_details(fields, features, detail_text):
    amount_min, amount_max = parse_range(field_value(fields, 'Сумма'), money=True)
    term_min, term_max = parse_term_range(field_value(fields, 'Срок'), 'months')
    rate_min, rate_max = parse_range(field_value(fields, 'Ставка'))
    gesv_min, gesv_max = parse_range(field_value(fields, 'ГЭСВ'))
    return {
        'amount_min': amount_min,
        'amount_max': amount_max,
        'term_min_months': term_min,
        'term_max_months': term_max,
        'rate_min': rate_min,
        'rate_max': rate_max,
        'gesv_min': gesv_min,
        'gesv_max': gesv_max,
        'purpose': extract_label(detail_text, 'Цель'),
        'income_proof_required': parse_income_proof(features, detail_text),
        'collateral': extract_label(detail_text, 'Обеспечение'),
        'passport_only': has_feature(features, 'только паспорт'),
    }


def build_mortgage_details(fields, features, detail_text):
    amount_min, amount_max = parse_range(field_value(fields, 'Сумма'), money=True)
    term_min, term_max = parse_term_range(field_value(fields, 'Срок'), 'months')
    rate_min, rate_max = parse_range(field_value(fields, 'Ставка'))
    gesv_min, gesv_max = parse_range(field_value(fields, 'ГЭСВ'))
    down_min, down_max = parse_range(field_value(fields, 'Первый взнос', 'Перв. взнос'))
    return {
        'amount_min': amount_min,
        'amount_max': amount_max,
        'term_min_months': term_min,
        'term_max_months': term_max,
        'rate_min': rate_min,
        'rate_max': rate_max,
        'gesv_min': gesv_min,
        'gesv_max': gesv_max,
        'down_payment_min': down_min,
        'down_payment_max': down_max,
        'purpose': extract_label(detail_text, 'Цель ипотеки'),
        'property_category': extract_label(detail_text, 'Категория недвижимости'),
        'collateral': extract_label(detail_text, 'Залог'),
        'insurance_required': parse_insurance(detail_text),
        'state_support': has_feature(features, 'Господдержка') or 'Господдержка' in detail_text,
    }


def build_credit_card_details(fields, features, detail_text):
    limit_min, limit_max = parse_range(field_value(fields, 'Кредитный лимит', 'Лимит'), money=True)
    grace_min, grace_max = parse_term_range(field_value(fields, 'Льготный период'), 'days')
    rate_min, rate_max = extract_percent_after_label(detail_text, 'Ставка')
    service_min, service_max = parse_range(field_value(fields, 'Обслуживание'), money=True)
    cashback, partner_cashback = parse_cashback(features)
    return {
        'limit_min': limit_min,
        'limit_max': limit_max,
        'grace_period_min_days': grace_min,
        'grace_period_max_days': grace_max,
        'rate_min': rate_min,
        'rate_max': rate_max,
        'issuance_fee': Decimal('0') if has_feature(features, 'Бесплатный выпуск') else None,
        'service_fee': service_max if service_max is not None else service_min,
        'service_period': parse_service_period(field_value(fields, 'Обслуживание')),
        'cashback_max': cashback,
        'partner_cashback_max': partner_cashback,
        'payment_system': extract_payment_system(detail_text),
        'card_class': extract_card_class(detail_text),
        'income_proof_required': parse_income_proof(features, detail_text),
        'installment': has_feature(features, 'рассрочк'),
        'free_notifications': has_feature(features, 'Бесплатные уведомления'),
        'courier_delivery': has_feature(features, 'Доставка курьером'),
        'free_cash_withdrawal': has_feature(features, 'Бесплатное снятие наличных'),
    }


def build_debit_card_details(fields, features, detail_text):
    interest_min, interest_max = parse_range(field_value(fields, 'Проценты на остаток'))
    service_min, service_max = parse_range(field_value(fields, 'Обслуживание'), money=True)
    cashback, partner_cashback = parse_cashback(features)
    return {
        'balance_interest_min': interest_min,
        'balance_interest_max': interest_max,
        'issuance_fee': Decimal('0') if has_feature(features, 'Бесплатный выпуск') else None,
        'service_fee_first_year': service_max if service_max is not None else service_min,
        'service_fee_next_year': extract_next_year_service(detail_text),
        'savings_account': parse_yes_no(field_value(fields, 'Накопительный счёт', 'Накопительный счет')),
        'cashback_max': cashback,
        'partner_cashback_max': partner_cashback,
        'payment_system': extract_payment_system(detail_text),
        'card_class': extract_card_class(detail_text),
        'free_notifications': has_feature(features, 'Бесплатные уведомления'),
        'courier_delivery': has_feature(features, 'Доставка курьером'),
        'cash_withdrawal_tariffs': [],
    }


def extract_label(text, label):
    match = re.search(rf'{re.escape(label)}:\s*([^:]+?)(?=\s+[А-ЯЁ][^:]{1,40}:|\s+(?:Без|С|Отправить)\b)', text)
    return clean_text(match.group(1))[:500] if match else ''


def extract_percent_after_label(text, label):
    match = re.search(rf'{re.escape(label)}\s+(?:от\s+)?([\d,.]+)(?:\s*[-–]\s*([\d,.]+))?\s*%', text)
    if not match:
        return None, None
    first = Decimal(match.group(1).replace(',', '.'))
    second = Decimal(match.group(2).replace(',', '.')) if match.group(2) else first
    return first, second


def parse_income_proof(features, detail_text):
    combined = ' '.join(features) + ' ' + detail_text[:3000]
    lowered = combined.lower()
    if 'без справ' in lowered or 'без подтверждения дохода' in lowered:
        return False
    if 'подтверждение дохода: требуется' in lowered:
        return True
    return None


def parse_insurance(text):
    lowered = text[:3000].lower()
    if 'без страхования' in lowered:
        return False
    if 'страхование обязательно' in lowered:
        return True
    return None


def parse_cashback(features):
    text = ' '.join(feature for feature in features if 'кэшбек' in feature.lower() or 'cashback' in feature.lower())
    values = parse_numeric_values(text)
    if not values:
        return None, None
    partner = values[-1] if 'партн' in text.lower() else None
    regular = values[0]
    return regular, partner


def parse_service_period(text):
    lowered = clean_text(text).lower()
    if 'месяц' in lowered:
        return 'month'
    if 'год' in lowered:
        return 'year'
    return ''


def parse_yes_no(text):
    lowered = clean_text(text).lower()
    if lowered == 'да':
        return True
    if lowered == 'нет':
        return False
    return None


def extract_payment_system(text):
    values = [value for value in ('Visa', 'Mastercard', 'MasterCard', 'UnionPay') if value.lower() in text.lower()]
    return ', '.join(dict.fromkeys(values))[:100]


def extract_card_class(text):
    for value in ('World Elite', 'Infinite', 'Platinum', 'Gold', 'Classic'):
        if value.lower() in text.lower():
            return value
    return ''


def extract_next_year_service(text):
    match = re.search(r'начиная со второго года\s+([\d\s]+)\s*₸', text, re.IGNORECASE)
    if not match:
        return None
    return Decimal(match.group(1).replace(' ', ''))
