<script setup lang="ts">
import {
  mdiAlertCircleOutline,
  mdiCardAccountDetailsOutline,
  mdiCheckCircleOutline,
  mdiChevronDown,
  mdiChevronUp,
  mdiCloseCircleOutline,
  mdiLayersOutline,
  mdiMagnify,
  mdiOpenInNew,
  mdiTuneVariant
} from '@mdi/js'
import {
  banks,
  filterConditions,
  marketplaceInfo,
  marketplaceTabs,
  type FilterTag,
  type MarketplaceTabId
} from '../data/marketplace'

const route = useRoute()
const activeTab = ref<MarketplaceTabId>('credits')
const search = ref('')
const openBanks = reactive<Record<string, boolean>>({})
const showFilter = ref(false)
const filters = reactive<{ type: string, tags: FilterTag[] }>({
  type: 'Потребительский',
  tags: []
})

const calcMode = ref<'new' | 'existing'>('new')
const amount = ref(3_000_000)
const months = ref(24)
const rate = ref(20)

const activeInfo = computed(() => marketplaceInfo[activeTab.value])
const filteredBanks = computed(() => banks.filter((bank) => {
  const matchesSearch = bank.name.toLowerCase().includes(search.value.trim().toLowerCase())
  const matchesTags = filters.tags.every(tag => bank.tags.includes(tag))
  return matchesSearch && matchesTags
}))

const result = computed(() => {
  const safeAmount = Math.max(50_000, Number(amount.value) || 50_000)
  const safeMonths = Math.max(3, Number(months.value) || 3)
  const monthlyRate = Math.max(0, Number(rate.value) || 0) / 100 / 12
  const monthly = monthlyRate === 0
    ? safeAmount / safeMonths
    : safeAmount * monthlyRate * (1 + monthlyRate) ** safeMonths / ((1 + monthlyRate) ** safeMonths - 1)
  const total = monthly * safeMonths
  return {
    monthly: Math.round(monthly),
    total: Math.round(total),
    overpay: Math.max(0, Math.round(total - safeAmount))
  }
})

const overpayPercent = computed(() => Math.round(result.value.overpay / Math.max(amount.value, 1) * 100))
const principalWidth = computed(() => `${Math.min(amount.value / Math.max(result.value.total, 1) * 100, 100)}%`)
const overpayWidth = computed(() => `${Math.min(result.value.overpay / Math.max(result.value.total, 1) * 100, 100)}%`)
const fmt = (value: number) => value.toLocaleString('ru-RU')

function toggleFilterTag(tag: FilterTag) {
  const index = filters.tags.indexOf(tag)
  if (index === -1) filters.tags.push(tag)
  else filters.tags.splice(index, 1)
}

function resetFilters() {
  filters.type = 'Потребительский'
  filters.tags.splice(0)
}

function clampCalculator() {
  amount.value = Math.min(5_000_000, Math.max(50_000, Number(amount.value) || 50_000))
  months.value = Math.min(120, Math.max(3, Number(months.value) || 3))
  rate.value = Math.min(56, Math.max(5, Number(rate.value) || 5))
}

function closeFilter() {
  showFilter.value = false
}

onMounted(() => {
  if (route.hash === '#calculator') {
    setTimeout(() => document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100)
  }
})

watch(showFilter, (open) => {
  if (import.meta.client) document.body.style.overflow = open ? 'hidden' : ''
})

onBeforeUnmount(() => {
  if (import.meta.client) document.body.style.overflow = ''
})
</script>

<template>
  <div class="mp-page">
    <section class="mp-hero">
      <img src="/bg-mrkp.svg" alt="" class="mp-hero__bg">
      <h1 class="mp-hero__title">Финансовый маркетплейс</h1>
      <p class="mp-hero__sub">
        Сравнивайте банковские продукты осознанно — с прозрачными условиями,
        расчётами и официальной информацией
      </p>
      <div class="mp-hero__notice">
        <MdiIcon :path="mdiAlertCircleOutline" :size="20" />
        <div>
          <p><strong>FinGramota не продаёт финансовые продукты и не принимает заявки.</strong></p>
          <p>Платформа помогает понять условия банков, сравнить предложения и избежать скрытых переплат.</p>
        </div>
      </div>
    </section>

    <div class="mp-tabs-bar">
      <div class="mp-tabs">
        <button
          v-for="tab in marketplaceTabs"
          :key="tab.id"
          type="button"
          class="mp-tab"
          :class="{ 'mp-tab--active': activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          <MdiIcon :path="tab.icon" :size="18" />
          {{ tab.label }}
        </button>
      </div>
    </div>

    <section class="mp-section">
      <h2 class="mp-section__title">{{ activeInfo.title }}</h2>
      <p class="mp-section__sub">{{ activeInfo.subtitle }}</p>

      <TransitionGroup name="mp-list" tag="div" class="mp-tips">
        <article v-for="tip in activeInfo.tips" :key="`${activeTab}-${tip.text}`" class="mp-tip">
          <div class="mp-tip__icon" :class="`mp-tip__icon--${tip.color}`">
            <MdiIcon :path="tip.icon" :size="22" />
          </div>
          <p>{{ tip.text }}</p>
        </article>
      </TransitionGroup>

      <div class="mp-search-row">
        <label class="mp-search-wrap">
          <MdiIcon :path="mdiMagnify" :size="20" />
          <input v-model="search" class="mp-search" type="search" aria-label="Поиск банка">
        </label>
        <button type="button" class="mp-filter-btn" @click="showFilter = true">
          <MdiIcon :path="mdiTuneVariant" :size="18" />
          Фильтр
        </button>
      </div>

      <div class="mp-banks">
        <article v-for="bank in filteredBanks" :key="bank.id" class="mp-bank">
          <button
            type="button"
            class="mp-bank__head"
            :aria-expanded="Boolean(openBanks[bank.id])"
            @click="openBanks[bank.id] = !openBanks[bank.id]"
          >
            <span class="mp-bank__name">{{ bank.name }}</span>
            <MdiIcon :path="openBanks[bank.id] ? mdiChevronUp : mdiChevronDown" :size="24" />
          </button>

          <Transition name="mp-accordion">
            <div v-if="openBanks[bank.id]" class="mp-bank__body">
              <div class="mp-bank__params">
                <span><strong>Сумма:</strong> {{ bank.amount }}</span>
                <span><strong>Ставка:</strong> {{ bank.rate }}</span>
                <span><strong>Срок:</strong> {{ bank.term }}</span>
                <span><strong>ГЭСВ:</strong> {{ bank.gesv }}</span>
              </div>
              <div class="mp-bank__features-head">
                <div class="mp-bank__feat-icon"><MdiIcon :path="mdiCardAccountDetailsOutline" :size="18" /></div>
                <strong>Особенности</strong>
              </div>
              <ul class="mp-bank__features">
                <li v-for="feature in bank.features" :key="feature">
                  <MdiIcon :path="mdiCheckCircleOutline" :size="18" />
                  {{ feature }}
                </li>
              </ul>
              <div class="mp-bank__note">
                <p><strong>ВАЖНО:</strong> {{ bank.note }}</p>
                <a :href="bank.link" target="_blank" rel="noopener noreferrer" class="mp-bank__link">
                  <MdiIcon :path="mdiOpenInNew" :size="16" />
                  Ссылка
                </a>
              </div>
            </div>
          </Transition>
        </article>
        <div v-if="!filteredBanks.length" class="mp-banks__empty">
          Банки не найдены. Измените параметры поиска или фильтры.
        </div>
      </div>
    </section>

    <section id="calculator" class="mp-calc-section">
      <img src="/bg-mrkp-calc.svg" alt="" class="mp-calc__bg">
      <h2 class="mp-calc__title">Калькулятор кредита</h2>
      <p class="mp-calc__sub">Halyk Bank — потребительский кредит — ГЭСВ до 25%</p>

      <div class="mp-calc-card">
        <p class="mp-calc__mode-label">Ваша ситуация</p>
        <div class="mp-calc__modes">
          <button type="button" class="mp-calc__mode" :class="{ 'mp-calc__mode--active': calcMode === 'new' }" @click="calcMode = 'new'">
            <MdiIcon :path="mdiCloseCircleOutline" :size="22" />
            <div><strong>Хочу взять кредит</strong><span>Ещё нет кредита в этом банке</span></div>
          </button>
          <button type="button" class="mp-calc__mode" :class="{ 'mp-calc__mode--active': calcMode === 'existing' }" @click="calcMode = 'existing'">
            <MdiIcon :path="mdiLayersOutline" :size="22" />
            <div><strong>У меня уже есть кредит</strong><span>Хочу понять переплату или досрочку</span></div>
          </button>
        </div>

        <div class="mp-calc__body">
          <div class="mp-calc__left">
            <div class="mp-calc__field">
              <div class="mp-calc__field-head">
                <label for="credit-amount">Сумма кредита</label>
                <div class="mp-calc__input-wrap"><input id="credit-amount" v-model.number="amount" type="number" @blur="clampCalculator"><span>₸</span></div>
              </div>
              <input v-model.number="amount" class="mp-calc__range" type="range" min="50000" max="5000000" step="50000">
              <div class="mp-calc__range-labels"><span>50 тыс</span><span>5 млн</span></div>
            </div>
            <div class="mp-calc__field">
              <div class="mp-calc__field-head">
                <label for="credit-months">Срок</label>
                <div class="mp-calc__input-wrap"><input id="credit-months" v-model.number="months" type="number" @blur="clampCalculator"><span>мес</span></div>
              </div>
              <input v-model.number="months" class="mp-calc__range" type="range" min="3" max="120">
              <div class="mp-calc__range-labels"><span>3 мес</span><span>120 мес</span></div>
            </div>
            <div class="mp-calc__field">
              <div class="mp-calc__field-head">
                <label for="credit-rate">Процентная ставка</label>
                <div class="mp-calc__input-wrap"><input id="credit-rate" v-model.number="rate" type="number" @blur="clampCalculator"><span>%</span></div>
              </div>
              <input v-model.number="rate" class="mp-calc__range" type="range" min="5" max="56">
              <div class="mp-calc__range-labels"><span>5%</span><span>56% (макс)</span></div>
            </div>
          </div>

          <div class="mp-calc__right">
            <div class="mp-calc__results">
              <div class="mp-calc__result-item"><span>Ежемесячный платёж</span><strong>{{ fmt(result.monthly) }} ₸</strong></div>
              <div class="mp-calc__result-item"><span>Общая выплата</span><strong>{{ fmt(result.total) }} ₸</strong></div>
              <div class="mp-calc__result-item mp-calc__result-item--gold"><span>Переплата</span><strong>{{ fmt(result.overpay) }} ₸</strong></div>
              <div class="mp-calc__result-item mp-calc__result-item--gold"><span>Ставка ГЭСВ</span><strong>{{ rate }}%</strong></div>
            </div>
            <div class="mp-calc__bars">
              <div class="mp-calc__bar-row"><span>Основной долг</span><span>{{ fmt(amount) }} ₸</span></div>
              <div class="mp-calc__bar-track"><div class="mp-calc__bar-fill mp-calc__bar-fill--navy" :style="{ width: principalWidth }" /></div>
              <div class="mp-calc__bar-row mp-calc__bar-row--spaced"><span>Переплата (проценты)</span><span>{{ fmt(result.overpay) }} ₸</span></div>
              <div class="mp-calc__bar-track"><div class="mp-calc__bar-fill mp-calc__bar-fill--red" :style="{ width: overpayWidth }" /></div>
            </div>
            <p class="mp-calc__advice">
              Переплата — {{ overpayPercent }}% от суммы. Чем короче срок, тем меньше итоговая переплата —
              попробуйте сдвинуть ползунок срока влево.
            </p>
          </div>
        </div>
      </div>
    </section>

    <Teleport to="body">
      <Transition name="mp-modal">
        <div v-if="showFilter" class="mp-filter-overlay" @click.self="closeFilter">
          <div class="mp-filter-panel" role="dialog" aria-modal="true" aria-labelledby="filter-title">
            <div class="mp-filter-head">
              <div><h3 id="filter-title">Фильтр банков</h3><p>Найдено {{ filteredBanks.length }} банков</p></div>
              <button type="button" class="mp-filter-reset" @click="resetFilters">Сбросить</button>
            </div>
            <div class="mp-filter-body">
              <div class="mp-filter-section">
                <h4>Тип кредита</h4>
                <div class="mp-filter-types">
                  <button
                    v-for="type in ['Потребительский', 'Авто', 'Микрокредит']"
                    :key="type"
                    type="button"
                    class="mp-filter-type-btn"
                    :class="{ 'mp-filter-type-btn--active': filters.type === type }"
                    @click="filters.type = type"
                  >{{ type }}</button>
                </div>
              </div>
              <div class="mp-filter-section">
                <h4>Условия оформления</h4>
                <button v-for="condition in filterConditions" :key="condition.key" type="button" class="mp-filter-check" @click="toggleFilterTag(condition.key)">
                  <span class="mp-filter-check__box" :class="{ 'mp-filter-check__box--checked': filters.tags.includes(condition.key) }">
                    <MdiIcon v-if="filters.tags.includes(condition.key)" :path="mdiCheckCircleOutline" :size="14" />
                  </span>
                  <span><span class="mp-filter-check__label">{{ condition.label }}</span><span class="mp-filter-check__sub">{{ condition.sub }}</span></span>
                </button>
              </div>
              <div class="mp-filter-section">
                <h4>Страхование депозитов (КФГД)</h4>
                <button type="button" class="mp-filter-check" @click="toggleFilterTag('kfgd')">
                  <span class="mp-filter-check__box" :class="{ 'mp-filter-check__box--checked': filters.tags.includes('kfgd') }">
                    <MdiIcon v-if="filters.tags.includes('kfgd')" :path="mdiCheckCircleOutline" :size="14" />
                  </span>
                  <span><span class="mp-filter-check__label">Только участники КФГД</span><span class="mp-filter-check__sub">Вклады защищены государством в пределах установленных лимитов</span></span>
                </button>
              </div>
            </div>
            <button type="button" class="mp-filter-apply" @click="closeFilter">Показать банки</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
