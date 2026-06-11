<script setup lang="ts">
import { mdiAlertOutline, mdiChevronRight, mdiFileDocumentCheckOutline, mdiMagnify } from '@mdi/js'

const query = ref('')
const activeId = ref<'license' | 'pyramid'>('license')
const types = [
  { id: 'license' as const, icon: mdiFileDocumentCheckOutline, label: 'Проверка лицензии', placeholder: 'Название компании, номер лицензии, БИН, адрес сайта' },
  { id: 'pyramid' as const, icon: mdiAlertOutline, label: 'Проверка финансовых пирамид', placeholder: 'Название, БИН/ИИН, адрес сайта, ФИО основателя проекта' }
]
const active = computed(() => types.find(item => item.id === activeId.value)!)
const training = [
  '4 сценария на основе реальных случаев в Казахстане',
  'Чат или звонок — выбирайте как реагировать',
  'Симуляция реального сценария мошенничества',
  'Живой индикатор угрозы и разбор красных флагов'
]
</script>

<template>
  <div>
    <section class="heroBanner"><div class="bgImage revealFade revealFadeVisible"><img src="/13-background.svg" alt="" class="bgImg"></div><div class="content"><h1 class="title reveal revealVisible">Перехват —<br>остановите риск<br>до потери денег</h1><p class="sub reveal revealVisible">Проверьте компанию, номер телефона или сайт за 10 секунд</p><div class="inputRow reveal revealVisible"><input v-model="query" class="input" placeholder="Введите БИН / ИИН / номер / сайт"><button class="btn"><MdiIcon :path="mdiMagnify" :size="18" />Проверить</button></div></div></section>
    <section class="section"><div class="header reveal revealVisible"><h2 class="title">Центр проверки</h2><p class="subtitle">Выберите тип проверки и получите мгновенную диагностику</p></div><div class="body"><aside class="sidebar reveal revealVisible"><p class="sidebarLabel">Типы проверки</p><ul class="typeList"><li v-for="type in types" :key="type.id"><button class="typeBtn" :class="{ typeBtnActive: activeId === type.id }" @click="activeId = type.id; query = ''"><span class="typeBtnIcon"><MdiIcon :path="type.icon" :size="22" /></span><span class="typeBtnLabel">{{ type.label }}</span><MdiIcon v-if="activeId === type.id" class="typeBtnArrow" :path="mdiChevronRight" :size="18" /></button></li></ul></aside><div class="panel reveal revealVisible"><h3 class="panelTitle">{{ active.label }}</h3><div class="inputRow"><input v-model="query" class="input" :placeholder="active.placeholder"><button class="btn" :disabled="!query.trim()"><MdiIcon :path="mdiMagnify" :size="18" />Проверить</button></div><div class="emptyState"><MdiIcon :path="mdiMagnify" :size="48" color="#c8c6d8" /><p>Введите данные для проверки</p></div></div></div></section>
    <section class="trainerBanner"><div class="trainerInner"><div class="trainerHeader reveal revealVisible"><h2 class="trainerTitle">Тренажёр бдительности</h2><p class="trainerSubtitle">Чат-симулятор: мошенник пишет вам в реальном времени, индикатор угрозы нарастает с каждым ходом.</p><button class="trainerButton">Начать тренировку</button></div><div class="trainerGrid"><article v-for="(card, index) in training" :key="card" class="trainerCard reveal revealVisible" :class="index === 0 || index === 3 ? 'trainerCardDark' : 'trainerCardLight'"><div class="trainerIcon"><MdiIcon :path="mdiAlertOutline" :size="24" /></div><div><h3>{{ card }}</h3><p>Практический сценарий с мгновенным разбором ответа и рекомендациями.</p></div></article></div></div></section>
  </div>
</template>
