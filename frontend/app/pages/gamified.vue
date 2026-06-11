<script setup lang="ts">
import { mdiCheck, mdiEmailOutline, mdiGiftOutline, mdiLockOutline, mdiPlay } from '@mdi/js'

const levels = [
  { n: 1, type: 'blue', icon: mdiCheck, title: 'Запрос пользователя' },
  { n: 2, type: 'green', icon: mdiCheck, title: 'Безопасные пароли' },
  { n: 3, type: 'red', icon: mdiEmailOutline, title: 'Что такое фишинг?', play: true },
  { n: 4, type: 'gray', icon: mdiLockOutline, title: 'Безопасность в соцсетях' },
  { n: 5, type: 'gray', icon: mdiLockOutline, title: 'Мобильная безопасность' },
  { n: 6, type: 'gray', icon: mdiLockOutline, title: 'Онлайн-покупки' },
  { n: 7, type: 'gray', icon: mdiLockOutline, title: 'Банковские карты' },
  { n: 8, type: 'gray', icon: mdiLockOutline, title: 'Защита данных' },
  { n: 9, type: 'gray', icon: mdiLockOutline, title: 'Финансовые риски' },
  { n: 10, type: 'gray', icon: mdiLockOutline, title: 'Что делать при атаке?' }
]
</script>

<template>
  <div class="gamified-page">
    <section class="gamified-hero"><div class="gamified-hero-inner"><div class="gamified-hero-text"><h1>Твое<br>приключение в<br>мире финансов!</h1><p>Проходи уровни, зарабатывай бонусы и стань экспертом цифровой безопасности</p></div><img class="gamified-robot" src="/happy retro robot.svg" alt="Робот"><div class="gamified-progress-card"><div class="gamified-progress-top"><span>Твой прогресс</span><b>3/20</b></div><div class="gamified-progress-line"><div class="gamified-progress-fill" /></div><p>Еще 17 уровней до мастера!</p></div></div></section>
    <section class="game-map-section"><div class="game-map-inner flex flex-col items-center gap-20 py-20"><div v-for="level in levels" :key="level.n" class="map-item !relative !left-auto !top-auto flex items-center gap-8" :class="{ 'flex-row-reverse': level.n % 2 === 0 }"><div class="map-circle" :class="level.type"><MdiIcon :path="level.icon" :size="46" /><span class="level-number">{{ level.n }}</span><span v-if="level.type !== 'gray'" class="coin-badge">3</span><span v-if="level.play" class="play-badge"><MdiIcon :path="mdiPlay" :size="20" /></span></div><div class="map-card !relative !left-auto !right-auto" :class="level.n % 2 ? 'left' : 'right'"><span>Уровень {{ level.n }}</span><h3>{{ level.title }}</h3><div v-if="level.n < 3" class="stars">★ ★ ★</div></div></div></div></section>
    <section class="bonus-section"><div class="bonus-card"><div class="bonus-circle" /><h2>Бонусы Halyk Bank!</h2><p class="bonus-subtitle">За каждый пройденный уровень</p><div class="bonus-list"><div class="bonus-item"><div class="bonus-value">+50</div><div class="bonus-label">баллов</div></div><div class="bonus-item"><div class="bonus-value">+10%</div><div class="bonus-label">кэшбек</div></div><div class="bonus-item"><div class="bonus-gift"><MdiIcon :path="mdiGiftOutline" :size="34" /></div><div class="bonus-label">подарки</div></div></div></div></section>
  </div>
</template>
