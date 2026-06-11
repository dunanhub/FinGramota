<script setup lang="ts">
import type { HTMLAttributes } from 'vue'

withDefaults(defineProps<{
  path: string
  size?: number | string
  class?: HTMLAttributes['class']
  color?: string
}>(), {
  size: 24,
  class: '',
  color: undefined
})
</script>

<template>
  <svg
    :class="$props.class"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="currentColor"
    :style="{ color }"
    aria-hidden="true"
  >
    <path :d="path" />
  </svg>
</template>
