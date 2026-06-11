<script setup lang="ts">
import { mdiCheckCircleOutline, mdiMagnify } from '@mdi/js'
import { faqCategories, faqSections } from '../data/faq'

const activeCategory = ref(faqCategories[0]!.label)
const search = ref('')
const question = ref('')
const sent = ref(false)
let sentTimer: ReturnType<typeof setTimeout> | undefined

const currentSection = computed(() => faqSections.find(section => section.category === activeCategory.value))
const filteredItems = computed(() => {
  const query = search.value.trim().toLocaleLowerCase('ru')
  if (!currentSection.value) return []
  if (!query) return currentSection.value.items
  return currentSection.value.items.filter(item =>
    `${item.question} ${item.answer}`.toLocaleLowerCase('ru').includes(query)
  )
})

function selectCategory(category: string) {
  activeCategory.value = category
  search.value = ''
}

function sendQuestion() {
  if (!question.value.trim()) return
  sent.value = true
  question.value = ''
  if (sentTimer) clearTimeout(sentTimer)
  sentTimer = setTimeout(() => { sent.value = false }, 3000)
}

onBeforeUnmount(() => {
  if (sentTimer) clearTimeout(sentTimer)
})
</script>

<template>
  <div class="faq-page">
    <section class="faq-hero">
      <div class="faq-hero__inner">
        <div class="faq-hero__copy">
          <h1>Часто задаваемые<br>вопросы</h1>
          <p>Найдите быстрые ответы на свои вопросы о финансовых инструментах и безопасности.</p>
          <label class="faq-search">
            <input v-model="search" type="search" placeholder="Опишите вашу проблему или задайте вопрос...">
            <MdiIcon :path="mdiMagnify" :size="26" />
          </label>
        </div>

        <form class="faq-question-card" @submit.prevent="sendQuestion">
          <h2>Задать вопрос</h2>
          <textarea v-model="question" rows="5" placeholder="Опишите вашу ситуацию..." />
          <button type="submit" :disabled="!question.trim()">
            <MdiIcon v-if="sent" :path="mdiCheckCircleOutline" :size="20" />
            {{ sent ? 'Отправлено!' : 'Отправить' }}
          </button>
        </form>
      </div>
    </section>

    <section class="faq-content">
      <div class="faq-content__inner">
        <nav class="faq-categories" aria-label="Категории вопросов">
          <button
            v-for="category in faqCategories"
            :key="category.label"
            type="button"
            class="faq-category"
            :class="{ 'faq-category--active': activeCategory === category.label }"
            @click="selectCategory(category.label)"
          >
            <span class="faq-category__dot" :style="{ backgroundColor: activeCategory === category.label ? '#ffffff' : category.dot }" />
            {{ category.label }}
          </button>
        </nav>

        <div v-if="currentSection" class="faq-results">
          <h2>{{ currentSection.title }}</h2>
          <TransitionGroup name="faq-list" tag="div" class="faq-list">
            <FaqAccordion
              v-for="item in filteredItems"
              :key="`${activeCategory}-${item.question}`"
              :question="item.question"
              :answer="item.answer"
            />
          </TransitionGroup>
          <div v-if="!filteredItems.length" class="faq-empty">
            По вашему запросу в этой категории ничего не найдено.
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
