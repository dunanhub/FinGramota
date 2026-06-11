<script setup lang="ts">
import { mdiArrowRight, mdiBookOpenPageVariantOutline, mdiCheckCircleOutline, mdiClockOutline } from '@mdi/js'
import type { Course } from '../../data/courses'

defineProps<{ course: Course }>()
</script>

<template>
  <article class="course-card">
    <div v-if="course.done || course.progress === 100" class="course-done" aria-label="Курс завершён"><MdiIcon :path="mdiCheckCircleOutline" :size="18" /></div>
    <span class="course-level" :class="course.color">{{ course.level }}</span>
    <h3>{{ course.title }}</h3>
    <div class="course-meta"><span><MdiIcon :path="mdiClockOutline" :size="14" />{{ course.hours }}</span><span><MdiIcon :path="mdiBookOpenPageVariantOutline" :size="14" />{{ course.lessons }}</span></div>
    <div class="course-progress-head"><span>Прогресс</span><b>{{ course.progress }}%</b></div>
    <div class="course-progress-track"><div class="course-progress-fill" :style="{ width: `${course.progress}%` }" /></div>
    <button class="course-btn">
      <span>{{ course.action ?? (course.progress === 0 ? 'Начать курс' : course.progress === 100 ? 'Повторить' : 'Продолжить') }}</span>
      <MdiIcon :path="mdiArrowRight" :size="16" />
    </button>
  </article>
</template>
