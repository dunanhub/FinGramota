<script setup lang="ts">
import { mdiEyeOffOutline, mdiEyeOutline } from '@mdi/js'

withDefaults(defineProps<{
  id: string
  placeholder: string
  autocomplete?: string
}>(), {
  autocomplete: 'current-password'
})

const model = defineModel<string>({ required: true })
const visible = ref(false)
</script>

<template>
  <div class="auth-input-wrap">
    <input
      :id="id"
      v-model="model"
      class="auth-input"
      :type="visible ? 'text' : 'password'"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
    >
    <button type="button" class="auth-eye" :aria-label="visible ? 'Скрыть пароль' : 'Показать пароль'" @click="visible = !visible">
      <MdiIcon :path="visible ? mdiEyeOffOutline : mdiEyeOutline" :size="22" />
    </button>
  </div>
</template>
