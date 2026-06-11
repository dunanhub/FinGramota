<script setup lang="ts">
import { mdiChevronDown } from '@mdi/js'

const props = defineProps<{ question: string, answer: string }>()
const open = ref(false)
const parts = computed(() => props.answer.split(/(https?:\/\/[^\s]+)/g).filter(Boolean))
const isLink = (part: string) => /^https?:\/\//.test(part)
</script>

<template>
  <article class="faq-accordion" :class="{ 'faq-accordion--open': open }">
    <button
      type="button"
      class="faq-accordion__trigger"
      :aria-expanded="open"
      @click="open = !open"
    >
      <span>{{ question }}</span>
      <MdiIcon :path="mdiChevronDown" :size="22" class="faq-accordion__chevron" />
    </button>
    <div class="faq-accordion__collapse">
      <div class="faq-accordion__overflow">
        <p class="faq-accordion__answer">
          <template v-for="(part, index) in parts" :key="index">
            <a v-if="isLink(part)" :href="part" target="_blank" rel="noopener noreferrer">{{ part }}</a>
            <template v-else>{{ part }}</template>
          </template>
        </p>
      </div>
    </div>
  </article>
</template>
