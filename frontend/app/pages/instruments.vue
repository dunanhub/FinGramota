<script setup lang="ts">
import { mdiChartLine, mdiShieldCheck } from '@mdi/js'

const tabs = ['Все', 'Расчёты', 'Проверки', 'Инвестиции', 'Безопасность']
const activeTab = ref('Все')
const tools = [
  ['Расчёты', 'Кредитный калькулятор', 'Рассчитайте ежемесячный платёж и общую сумму выплат по кредиту.', '/1-kalkulyator.jpg'],
  ['Проверки', 'Проверка брокера', 'Убедитесь, что у инвестиционной компании есть лицензия.', '/2-broker.jpg'],
  ['Проверки', 'Проверка лицензии', 'Единый реестр финансовых организаций с лицензиями.', '/3-licenziya.jpg'],
  ['Безопасность', 'Финансовая пирамида', 'Проверьте признаки сомнительной организации чек-листом.', '/4-piramida.jpg'],
  ['Безопасность', 'Проверка сайта', 'Выявление фишинговых сайтов и поддельных страниц.', '/5-sait.jpg'],
  ['Безопасность', 'Проверка телефона', 'Узнайте, есть ли номер в базе мошенников.', '/6-telefon.jpg'],
  ['Инвестиции', 'Доходность инвестиций', 'Сравните доходность вкладов, облигаций и акций.', '/7-dohodnost.jpg'],
  ['Расчёты', 'Долговая нагрузка', 'Оцените показатель DTI перед новым кредитом.', '/8-nagruzka.jpg']
]
const filteredTools = computed(() => activeTab.value === 'Все' ? tools : tools.filter(tool => tool[0] === activeTab.value))
</script>

<template>
  <div class="instruments-page">
    <section class="instruments-hero"><div class="instruments-hero-inner"><div class="instruments-hero-text"><div class="instruments-badge"><MdiIcon :path="mdiShieldCheck" :size="16" /><span>Центр инструментов</span></div><h1>Инструменты<br><span>финансовой защиты и расчёта</span></h1><p>Единый цифровой центр финансовой помощи, грамотности и защиты пользователей.</p></div><div class="instruments-hero-image"><img src="/инст.svg" alt="Финансовая защита"><div class="status-card"><div class="status-icon"><MdiIcon :path="mdiShieldCheck" :size="22" /></div><div class="status-content"><small>Статус</small><b>Безопасно</b></div></div><div class="load-card"><div class="load-icon"><MdiIcon :path="mdiChartLine" :size="18" /></div><small>Анализ нагрузки</small><div class="load-line"><span /></div><div class="load-info"><b>45%</b><span>Норма</span></div></div></div></div></section>
    <section class="tools-section"><div class="circle-decor circle-left" /><div class="circle-decor circle-right" /><div class="tools-inner"><h2>Сервисы</h2><div class="tools-tabs"><button v-for="tab in tabs" :key="tab" :class="{ active: activeTab === tab }" @click="activeTab = tab">{{ tab }}</button></div><TransitionGroup name="tools" tag="div" class="tools-grid"><article v-for="tool in filteredTools" :key="tool[1]" class="tool-card"><div class="tool-image"><img :src="tool[3]" :alt="tool[1]"></div><div class="tool-content"><div><h3>{{ tool[1] }}</h3><p>{{ tool[2] }}</p></div><button @click="tool[1] === 'Кредитный калькулятор' ? navigateTo('/marketplace#calculator') : navigateTo('/check')">Открыть</button></div></article></TransitionGroup></div></section>
  </div>
</template>

<style scoped>
.tools-enter-active,.tools-leave-active{transition:all .35s ease}.tools-enter-from,.tools-leave-to{opacity:0;transform:translateY(18px)}
</style>
