<script setup lang="ts">
import {
  mdiAlertOutline,
  mdiArrowRight,
  mdiArrowTopRight,
  mdiBookOpenPageVariantOutline,
  mdiCalculatorVariantOutline,
  mdiCardAccountDetailsOutline,
  mdiCheck,
  mdiCheckCircleOutline,
  mdiChevronLeft,
  mdiChevronRight,
  mdiCreditCardOutline,
  mdiEarHearing,
  mdiEyeOutline,
  mdiShieldCheckOutline,
  mdiWheelchairAccessibility
} from '@mdi/js'
import { useFinGramotaApi } from '../composables/useFinGramotaApi'
import { useRevealOnScroll } from '../composables/useReveal'

const featureCards = [
  {
    icon: mdiCreditCardOutline,
    title: 'Маркетплейс',
    text: 'Планирование доходов и расходов, финансовые цели и полезные привычки для стабильного бюджета.',
    path: '/marketplace'
  },
  {
    icon: mdiBookOpenPageVariantOutline,
    title: 'Обучение',
    text: 'Что важно учитывать перед оформлением кредита, как читать договор и оценивать условия.',
    path: '/education'
  },
  {
    icon: mdiShieldCheckOutline,
    title: 'Безопасность',
    text: 'Как распознать мошенничество, защитить карты, счета и персональные данные.',
    path: '/check'
  },
  {
    icon: mdiCardAccountDetailsOutline,
    title: 'Инструменты',
    text: 'Банковские карты, депозиты, страхование и другие финансовые услуги простым языком.',
    path: '/instruments'
  }
]

const interesting = [
  { title: 'Стоп кредит', text: 'Каждый гражданин может на неограниченное количество времени установить запрет на выдачу банковских займов и микрокредитов', image: '/interesting/stop-credit.svg' },
  { title: 'Европротокол', text: 'Позволит получить страховые выплаты дистанционно и оперативно, без привлечения дорожной полиции', image: '/interesting/europrotocol.svg' },
  { title: 'Рынок ценных бумаг', text: 'Знания, которые помогут принимать уверенные финансовые решения.', image: '/interesting/market.svg' },
  { title: 'Мошеннический кредит', text: 'С полученным постановлением необходимо обратиться к кредитору.', image: '/interesting/fraud-credit.svg' },
  { title: 'Хочу разобраться в финансах', text: 'Знания, которые помогут принимать уверенные финансовые решения.', image: '/interesting/finance.svg' },
  { title: 'Кто такие дропперы', text: 'Это лицо, которое предоставляет свои банковские реквизиты для проведения незаконных операций', image: '/interesting/dropper.svg' },
  { title: 'Страхование', text: 'Финансовая защита от возможных убытков или рисков.', image: '/interesting/insurance.svg' },
  { title: 'Оспаривания кредитной истории', text: 'Вы не согласны со своей кредитной историей и не знаете что делать, тогда эта статья для вас.', image: '/interesting/history.svg' }
]

const { target: introTarget, visible: introVisible } = useRevealOnScroll()
const { target: interestingTarget, visible: interestingVisible } = useRevealOnScroll()
const { target: newsTarget, visible: newsVisible } = useRevealOnScroll()
const { target: podcastTarget, visible: podcastVisible } = useRevealOnScroll()
const { target: inclusiveTarget, visible: inclusiveVisible } = useRevealOnScroll()

const { getHomeContent } = useFinGramotaApi()
const news = ref<Awaited<ReturnType<typeof getHomeContent>>['news']>([])
const podcasts = ref<Awaited<ReturnType<typeof getHomeContent>>['podcasts']>([])
const podcastTrack = ref<HTMLElement | null>(null)
let interval: ReturnType<typeof setInterval> | undefined

function scrollPodcasts(direction: 1 | -1) {
  const track = podcastTrack.value
  const card = track?.querySelector<HTMLElement>('.podcast-card')
  if (!track || !card) return

  const distance = card.offsetWidth + 28
  const maxScrollLeft = track.scrollWidth - track.clientWidth

  if (direction === 1 && track.scrollLeft >= maxScrollLeft - 10) {
    track.scrollTo({ left: 0, behavior: 'smooth' })
    return
  }

  track.scrollBy({ left: direction * distance, behavior: 'smooth' })
}

function staggerStyle(visible: boolean, index: number, step = 80) {
  return {
    opacity: visible ? 1 : 0,
    transform: visible ? 'translateY(0)' : 'translateY(22px)',
    transition: `opacity 0.55s ease ${index * step}ms, transform 0.55s ease ${index * step}ms`
  }
}

onMounted(async () => {
  const content = await getHomeContent()
  news.value = content.news
  podcasts.value = content.podcasts
  interval = setInterval(() => scrollPodcasts(1), 5000)
})

onBeforeUnmount(() => {
  if (interval) clearInterval(interval)
})
</script>

<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-left">
        <div class="portal-badge hero-reveal hero-delay-1">● ОФИЦИАЛЬНЫЙ ГОСУДАРСТВЕННЫЙ ПОРТАЛ</div>
        <h1 class="hero-reveal hero-delay-2">Повышение <span>финансовой</span> грамотности населения</h1>
        <p class="hero-reveal hero-delay-3">Научитесь разбираться в деньгах, кредитах и финансовой безопасности в повседневной жизни</p>

        <div class="hero-buttons hero-reveal hero-delay-4">
          <button class="sos-btn" @click="navigateTo('/sos')"><MdiIcon :path="mdiAlertOutline" :size="30" />SOS ситуация</button>
          <button class="start-btn" @click="navigateTo('/education')">Начать курс</button>
        </div>

        <div class="hero-points hero-reveal hero-delay-5">
          <span v-for="point in ['Бесплатно', 'Без рекламы', '100% анонимно']" :key="point"><MdiIcon :path="mdiCheckCircleOutline" :size="20" />{{ point }}</span>
        </div>
      </div>

      <div class="hero-center">
        <div class="hero-center-reveal hero-reveal hero-delay-3">
          <div class="circle circle-1" />
          <div class="circle circle-2" />
          <img src="/Vector (1).svg" alt="Защитный щит" class="hero-shield">
        </div>
      </div>

      <div class="license-card home-card-reveal">
        <div class="license-icon"><MdiIcon :path="mdiCheck" :size="30" /></div>
        <div><small>Статус проверки</small><b>Лицензия активна</b></div>
      </div>

      <div class="calc-card home-card-reveal home-card-reveal-late">
        <MdiIcon :path="mdiCalculatorVariantOutline" :size="42" />
        <div><small>Инструменты</small><b>Кредитный калькулятор</b></div>
      </div>
    </section>

    <section ref="introTarget" class="intro-section scroll-reveal" :class="{ 'is-visible': introVisible }">
      <div class="feature-grid">
        <article
          v-for="(card, index) in featureCards"
          :key="card.title"
          class="feature-card"
          :style="staggerStyle(introVisible, index, 90)"
        >
          <div class="feature-top"><MdiIcon :path="card.icon" :size="28" class="feature-icon" /><h3>{{ card.title }}</h3></div>
          <p>{{ card.text }}</p>
          <button class="more-btn" @click="navigateTo(card.path)"><span>Подробнее</span><MdiIcon :path="mdiArrowTopRight" :size="14" /></button>
        </article>
      </div>

      <div class="intro-text">
        <h2>Финансовая грамотность <span>простым языком</span></h2>
        <p>Портал создан для повышения финансовой грамотности населения и предоставляет актуальную и проверенную информацию.</p>
        <button class="hero-btn" @click="navigateTo('/marketplace#calculator')">Калькулятор</button>
      </div>
    </section>

    <section ref="interestingTarget" class="interesting-section scroll-reveal" :class="{ 'is-visible': interestingVisible }">
      <h2>Интересное</h2>
      <div class="interesting-grid">
        <article
          v-for="(item, index) in interesting"
          :key="item.title"
          class="interesting-card"
          :class="`card-${index + 1}`"
          :style="staggerStyle(interestingVisible, index, 70)"
        >
          <img class="interesting-bg-icon" :src="item.image" alt="">
          <div class="interesting-content"><h3>{{ item.title }}</h3><p>{{ item.text }}</p></div>
        </article>
      </div>
    </section>

    <section id="news" ref="newsTarget" class="news-section scroll-reveal" :class="{ 'is-visible': newsVisible }">
      <div class="section-head">
        <h2>Новости</h2>
        <p>Следите за последними новостями в сфере финансов и безопасности</p>
        <a href="#news">Все новости <MdiIcon :path="mdiArrowRight" :size="20" /></a>
      </div>
      <div class="news-grid">
        <article
          v-for="(item, index) in news.slice(0, 8)"
          :key="`${item.title}-${index}`"
          class="news-card"
          :class="{ large: index < 2 }"
          :style="staggerStyle(newsVisible, index, 70)"
        >
          <img :src="item.image" :alt="item.title">
          <div><h3>{{ item.title }}</h3><span>{{ item.date }}</span></div>
        </article>
      </div>
    </section>

    <section ref="podcastTarget" class="podcast-section scroll-reveal" :class="{ 'is-visible': podcastVisible }">
      <div class="podcast-header"><h2>Подкасты</h2><p>Слушайте полезные выпуски о финансах, безопасности и цифровой грамотности</p></div>
      <div class="podcast-slider">
        <div ref="podcastTrack" class="podcast-track">
          <article
            v-for="(item, index) in podcasts"
            :key="`${item.title}-${index}`"
            class="podcast-card"
            :style="staggerStyle(podcastVisible, index, 90)"
          >
            <img :src="item.image" :alt="item.title">
          </article>
        </div>
      </div>
      <div class="podcast-buttons">
        <button aria-label="Предыдущий подкаст" @click="scrollPodcasts(-1)"><MdiIcon :path="mdiChevronLeft" :size="36" /></button>
        <button aria-label="Следующий подкаст" @click="scrollPodcasts(1)"><MdiIcon :path="mdiChevronRight" :size="36" /></button>
      </div>
    </section>

    <section id="inclusive" ref="inclusiveTarget" class="inclusive-section scroll-reveal" :class="{ 'is-visible': inclusiveVisible }">
      <div class="inclusive-text">
        <h2>Инклюзивные финансы</h2>
        <p>Мы стремимся сделать финансовые услуги доступными для каждого. Наша интерактивная карта поможет вам найти отделения банков, оборудованные всем необходимым для людей с особыми потребностями.</p>
        <div class="inclusive-buttons">
          <button><MdiIcon :path="mdiWheelchairAccessibility" :size="30" />Пандусы и подъемники</button>
          <button><MdiIcon :path="mdiEyeOutline" :size="30" />Шрифт Брайля в терминалах</button>
          <button><MdiIcon :path="mdiEarHearing" :size="30" />Оборудование для слабослышащих</button>
        </div>
      </div>
      <div class="map"><img src="/map.svg" alt="Инклюзивная карта"></div>
    </section>
  </div>
</template>
