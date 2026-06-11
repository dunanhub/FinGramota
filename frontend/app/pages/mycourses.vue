<script setup lang="ts">
import { mdiChevronLeft, mdiChevronRight } from '@mdi/js'
import { courses } from '../data/courses'
</script>

<template>
  <div class="courses-page">
    <section class="courses-hero">
      <img src="/16-bcg_l_courses.svg" alt="" class="courses-hero__bg-left"><img src="/15-bcg_r_courses.svg" alt="" class="courses-hero__bg-right">
      <button class="courses-hero__back"><MdiIcon :path="mdiChevronLeft" :size="20" /></button>
      <div class="courses-hero__card courses-reveal courses-reveal--visible"><span class="courses-badge courses-badge--light">Изучается сейчас</span><h2 class="courses-hero__title">Основы финансовой безопасности</h2><p class="courses-hero__module">Модуль 4: Распределение вероятностей</p><div class="courses-hero__progress-row"><span>Прогресс курса</span><span class="courses-hero__pct">75%</span></div><div class="courses-progress-bar courses-progress-bar--dark"><div class="courses-progress-bar__fill" style="width:75%" /></div><button class="courses-hero__btn">Продолжить<MdiIcon :path="mdiChevronRight" :size="18" /></button></div>
    </section>
    <section class="courses-section"><h2 class="courses-section__title courses-reveal courses-reveal--visible">Ваши курсы</h2><p class="courses-section__sub courses-reveal courses-reveal--visible">Продолжите с того места, где остановились</p><div class="courses-grid"><CourseCard v-for="course in courses.slice(0, 4)" :key="course.id" :course="course" /></div></section>
  </div>
</template>
