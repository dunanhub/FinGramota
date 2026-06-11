<script setup lang="ts">
import { mdiCheck, mdiClockOutline, mdiContentCopy, mdiPhone } from '@mdi/js'
import { useClipboard } from '../../composables/useClipboard'

defineProps<{ icon: string, title: string, subtitle: string, hours: string, phone: string }>()
const { copied, copy } = useClipboard()
</script>

<template>
  <article class="sos-contact-card"><div class="sos-card-head"><div class="sos-icon-wrap"><MdiIcon :path="icon" :size="26" /></div><div><h3>{{ title }}</h3><p>{{ subtitle }}</p><div class="sos-hours"><MdiIcon :path="mdiClockOutline" :size="15" /><span>{{ hours }}</span></div></div></div><div class="sos-card-actions"><a class="sos-phone-btn" :href="`tel:${phone}`"><MdiIcon :path="mdiPhone" :size="18" />{{ phone }}</a><button class="sos-copy-btn" @click="copy(phone)"><MdiIcon :path="copied ? mdiCheck : mdiContentCopy" :size="18" /></button></div></article>
</template>
