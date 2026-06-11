import {
  mdiCancel,
  mdiCardAccountDetailsOutline,
  mdiChartLineVariant,
  mdiCreditCardOutline,
  mdiHomeOutline,
  mdiMagnify,
  mdiPiggyBankOutline,
  mdiTimerOutline,
  mdiTrendingUp
} from '@mdi/js'

export type MarketplaceTabId = 'credits' | 'deposits' | 'mortgage' | 'debit' | 'investments'
export type FilterTag = 'online' | 'no-pledge' | 'no-guarantor' | 'early' | 'kfgd'

export interface MarketplaceTip {
  color: 'red' | 'blue' | 'yellow' | 'green'
  icon: string
  text: string
}

export interface MarketplaceBank {
  id: string
  name: string
  amount: string
  rate: string
  term: string
  gesv: string
  features: string[]
  note: string
  link: string
  tags: FilterTag[]
}

export const marketplaceTabs: Array<{ id: MarketplaceTabId, label: string, icon: string }> = [
  { id: 'credits', label: 'Кредиты', icon: mdiCreditCardOutline },
  { id: 'deposits', label: 'Депозиты', icon: mdiPiggyBankOutline },
  { id: 'mortgage', label: 'Ипотека', icon: mdiHomeOutline },
  { id: 'debit', label: 'Дебетовые карты и счета', icon: mdiCardAccountDetailsOutline },
  { id: 'investments', label: 'Инвестиционные продукты', icon: mdiTrendingUp }
]

export const marketplaceInfo: Record<MarketplaceTabId, { title: string, subtitle: string, tips: MarketplaceTip[] }> = {
  credits: {
    title: 'Потребительские кредиты',
    subtitle: 'Кредит на личные расходы без залога: ремонт, техника, обучение, лечение или другие цели',
    tips: [
      { color: 'red', icon: mdiCancel, text: 'Низкая ставка — не всегда низкая переплата' },
      { color: 'blue', icon: mdiMagnify, text: 'Смотрите на ГЭСВ' },
      { color: 'yellow', icon: mdiTimerOutline, text: 'Чем длиннее срок — тем выше переплата' },
      { color: 'green', icon: mdiChartLineVariant, text: 'Досрочное погашение уменьшает переплату' }
    ]
  },
  deposits: {
    title: 'Депозиты',
    subtitle: 'Вклад для хранения денег и получения вознаграждения от банка',
    tips: [
      { color: 'red', icon: mdiCancel, text: 'Высокая ставка часто означает ограничения по снятию' },
      { color: 'blue', icon: mdiMagnify, text: 'Смотрите на ГЭСВ, а не только на номинальную ставку' },
      { color: 'yellow', icon: mdiTimerOutline, text: 'Депозиты гарантируются КФГД в пределах установленных лимитов' },
      { color: 'green', icon: mdiChartLineVariant, text: 'Проверьте возможность пополнения и частичного снятия' }
    ]
  },
  mortgage: {
    title: 'Ипотека',
    subtitle: 'Кредит на покупку жилья с первоначальным взносом и длительным сроком',
    tips: [
      { color: 'red', icon: mdiCancel, text: 'Условия зависят от типа жилья: первичное, вторичное или ДДУ' },
      { color: 'blue', icon: mdiMagnify, text: 'Сравнивайте ГЭСВ, а не только ставку' },
      { color: 'yellow', icon: mdiTimerOutline, text: 'Чем больше срок — тем выше итоговая переплата' },
      { color: 'green', icon: mdiChartLineVariant, text: 'Первоначальный взнос заметно влияет на платёж' }
    ]
  },
  debit: {
    title: 'Дебетовые карты и счета',
    subtitle: 'Карты для хранения денег, переводов, оплаты покупок и получения зарплаты',
    tips: [
      { color: 'red', icon: mdiCancel, text: 'Проверяйте комиссии за снятие и переводы' },
      { color: 'blue', icon: mdiMagnify, text: 'Уточняйте лимиты на бесплатные операции' },
      { color: 'yellow', icon: mdiTimerOutline, text: 'Кешбэк не важнее стоимости обслуживания и удобства' },
      { color: 'green', icon: mdiChartLineVariant, text: 'Сравнивайте стоимость годового обслуживания' }
    ]
  },
  investments: {
    title: 'Инвестиционные продукты',
    subtitle: 'Инструменты для покупки ценных бумаг, фондов и других финансовых активов',
    tips: [
      { color: 'red', icon: mdiCancel, text: 'Инвестиции не являются депозитом' },
      { color: 'blue', icon: mdiMagnify, text: 'Доходность не гарантирована' },
      { color: 'yellow', icon: mdiTimerOutline, text: 'Возможна потеря части или всей суммы' },
      { color: 'green', icon: mdiChartLineVariant, text: 'Проверяйте лицензию брокера и комиссии' }
    ]
  }
}

export const banks: MarketplaceBank[] = [
  {
    id: 'halyk', name: 'Halyk Bank', amount: 'до 8 000 000 ₸', rate: 'от 17.5%', term: 'до 60 месяцев', gesv: '39.10%',
    features: ['Онлайн-оформление через Homebank', 'Возможен кредит без справки о доходах', 'Бесплатное досрочное погашение', 'Для зарплатных клиентов условия лучше'],
    note: 'На сайте банка есть калькулятор, который поможет оценить условия.', link: 'https://homebank.kz',
    tags: ['online', 'no-pledge', 'early']
  },
  {
    id: 'kaspi', name: 'Kaspi Bank', amount: 'до 5 000 000 ₸', rate: 'от 19%', term: 'до 48 месяцев', gesv: '42.00%',
    features: ['Оформление через Kaspi.kz или приложение', 'Решение за 5 минут', 'Без поручителей и залога'],
    note: 'Один из самых быстрых кредитов — всё оформляется онлайн.', link: 'https://kaspi.kz',
    tags: ['online', 'no-pledge', 'no-guarantor']
  },
  {
    id: 'centercredit', name: 'CenterCredit Bank', amount: 'до 10 000 000 ₸', rate: 'от 16%', term: 'до 84 месяцев', gesv: '35.50%',
    features: ['Длительный срок кредитования', 'Возможно оформление с поручителем', 'Гибкий график погашения'],
    note: 'Подходит для крупных покупок с длительным сроком.', link: 'https://bcc.kz',
    tags: ['online', 'early']
  },
  {
    id: 'freedom', name: 'Freedom', amount: 'до 6 000 000 ₸', rate: 'от 18%', term: 'до 60 месяцев', gesv: '40.20%',
    features: ['Онлайн-заявка без визита в банк', 'Страхование по желанию', 'Досрочное погашение без штрафа'],
    note: 'Подходит для полностью дистанционного оформления.', link: 'https://ffin.kz',
    tags: ['online', 'no-pledge', 'early']
  },
  {
    id: 'bereke', name: 'Bereke Bank', amount: 'до 7 000 000 ₸', rate: 'от 20%', term: 'до 60 месяцев', gesv: '44.00%',
    features: ['Без залога и поручителей', 'Доступно онлайн-оформление', 'Возможна реструктуризация'],
    note: 'Подходит клиентам без зарплатной карты в крупных банках.', link: 'https://berekebank.kz',
    tags: ['online', 'no-pledge', 'no-guarantor']
  },
  {
    id: 'alatau', name: 'Alatau City Bank', amount: 'до 3 000 000 ₸', rate: 'от 22%', term: 'до 36 месяцев', gesv: '48.00%',
    features: ['Минимальный пакет документов', 'Для новых клиентов действуют специальные условия'],
    note: 'Небольшие суммы и быстрое рассмотрение.', link: 'https://alataucitybank.kz',
    tags: ['online']
  }
]

export const filterConditions: Array<{ key: FilterTag, label: string, sub: string }> = [
  { key: 'online', label: 'Онлайн-оформление', sub: 'Без визита в отделение' },
  { key: 'no-pledge', label: 'Без залога', sub: 'Не требуется имущество в обеспечение' },
  { key: 'no-guarantor', label: 'Без поручительства', sub: 'Только на основании дохода заёмщика' },
  { key: 'early', label: 'Досрочное погашение без штрафа', sub: 'Можно закрыть кредит раньше срока' }
]
