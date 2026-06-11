<script setup lang="ts">
import { mdiArrowRight, mdiCreationOutline, mdiMedalOutline, mdiShieldCheckOutline, mdiTrendingUp } from '@mdi/js'
import { courses } from '../data/courses'

const lessons = [75, 100, 60, 30]
</script>

<template>
  <div class="page-reveal">
    <section class="learning-hero">
      <div class="learning-content">
        <div class="learning-info"><h1>Финансовая<br>грамотность —<br>понятным языком</h1><p>Выберите формат и начните с вашей ситуации</p><button class="learning-start-btn"><MdiIcon :path="mdiCreationOutline" :size="18" />Начать обучение</button></div>
        <div class="learning-progress-card">
          <div class="learning-points"><MdiIcon :path="mdiMedalOutline" :size="20" />+50 баллов</div>
          <div class="learning-card-head"><div class="learning-icon-box"><MdiIcon :path="mdiShieldCheckOutline" :size="26" /></div><div><h3>Защита от мошенников</h3><span>Модуль 4 из 10</span></div></div>
          <div class="learning-lessons"><div v-for="(percent, index) in lessons" :key="index" class="learning-lesson"><div class="lesson-row"><span>Урок {{ index + 1 }}</span><span>{{ percent }}%</span></div><div class="lesson-track"><div class="lesson-fill" :style="{ width: `${percent}%` }" /></div></div></div>
          <div class="learning-total-progress"><MdiIcon :path="mdiTrendingUp" :size="20" />Прогресс: 65%</div>
        </div>
      </div>
    </section>
    <section class="online-courses-section"><div class="online-courses-inner"><h2>Онлайн курсы</h2><div class="courses-tabs"><button class="active">В тренде</button><button>Видео-уроки</button><button>Курсы</button><button>Игры</button></div><div class="courses-grid"><CourseCard v-for="course in courses" :key="course.id" :course="course" /></div></div></section>
    <section class="popular-section"><div class="popular-inner"><h2>Часто ищут</h2><p>Популярные направления обучения и востребованные навыки</p><div class="popular-grid"><article v-for="(item, index) in ['Личные финансы', 'Инвестиции', 'Банковские продукты', 'Кибербезопасность']" :key="item" class="popular-card" :class="index === 0 ? 'popular-card-tall' : index === 1 ? 'popular-card-wide' : 'popular-card-small'"><div><h3>{{ item }}</h3><span>{{ 70 + index * 15 }} курсов</span><p>Планирование, бюджет, накопления</p></div><button type="button" @click="navigateTo('/mycourses')"><span>Перейти</span><MdiIcon :path="mdiArrowRight" :size="18" /></button></article></div></div></section>
    <section class="recommended-courses-section">
      <div class="recommended-courses-inner">
        <h2>Рекомендованные курсы</h2>
        <p>Курсы, отобранные на основе ваших интересов и уровня подготовки</p>
        <div class="courses-grid">
          <CourseCard v-for="course in courses" :key="`recommended-${course.id}`" :course="course" />
        </div>
      </div>
    </section>
    <section class="kids-adventure-section"><div class="kids-adventure-inner"><div class="kids-adventure-content"><h2>Финансовое приключение для детей!</h2><p>Учимся распоряжаться деньгами в игровом формате</p><button class="kids-adventure-btn" @click="navigateTo('/gamified')">Перейти<MdiIcon :path="mdiArrowRight" :size="18" /></button></div><img class="kids-robot-img" src="/happy retro robot.svg" alt="Робот"></div></section>
  </div>
</template>
