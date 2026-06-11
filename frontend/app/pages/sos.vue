<script setup lang="ts">
import { mdiBank, mdiCheck, mdiContentCopy, mdiDownload, mdiFileDocumentOutline, mdiFlash, mdiPhone, mdiRobotOutline, mdiScaleBalance, mdiSend, mdiShieldCheck } from '@mdi/js'
import { emergencyContacts } from '../data/sos'
import { useClipboard } from '../composables/useClipboard'
import { useFinGramotaApi, type ChatMessage } from '../composables/useFinGramotaApi'

const { copied, copy } = useClipboard()
const input = ref('')
const loading = ref(false)
const messages = ref<ChatMessage[]>([{ role: 'agent', text: 'Здравствуйте! Опишите вашу ситуацию, и я подскажу первые шаги.', time: '09:00' }])
const { sendAgentMessage } = useFinGramotaApi()

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return
  messages.value.push({ role: 'user', text, time: new Date().toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }) })
  input.value = ''
  loading.value = true
  try {
    const reply = await sendAgentMessage(messages.value)
    messages.value.push({ role: 'agent', text: reply, time: new Date().toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }) })
  } catch {
    setTimeout(() => messages.value.push({ role: 'agent', text: 'Сначала заблокируйте карту или операцию, затем позвоните в банк и зафиксируйте обращение по номеру 1459.', time: new Date().toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }) }), 500)
  } finally {
    loading.value = false
  }
}

const documents = [
  { icon: mdiFileDocumentOutline, title: 'Заявление о мошенничестве', text: 'Шаблон для обращения в правоохранительные органы.', url: '/documents/Заявление.pdf' },
  { icon: mdiBank, title: 'Обращение в банк', text: 'Форма для срочной блокировки операции или карты.', url: '/documents/банкжалоба.pdf' },
  { icon: mdiScaleBalance, title: 'Жалоба регулятору', text: 'Документ для защиты прав потребителя финансовых услуг.', url: '#' }
]
</script>

<template>
  <div class="sos-page">
    <section class="sos-hero"><div class="sos-hero-inner"><div class="sos-hero-content"><div class="sos-badge"><MdiIcon :path="mdiFlash" :size="16" />Срочная помощь</div><h1>Столкнулись с<br><span>финансовой проблемой?</span></h1><p>Не паникуйте. Здесь собраны контакты и документы, которые помогут действовать быстро.</p></div><div class="sos-support-card"><MdiIcon :path="mdiShieldCheck" :size="48" /><small>Единый call-центр</small><strong>1459</strong><div><a href="tel:1459"><MdiIcon :path="mdiPhone" :size="18" />Позвонить</a><button @click="copy('1459')"><MdiIcon :path="copied ? mdiCheck : mdiContentCopy" :size="18" /></button></div></div></div></section>
    <section class="sos-contacts-section"><div class="sos-inner"><div class="sos-section-header"><h2>Экстренные контакты</h2><p>Свяжитесь с нужной организацией напрямую</p></div><div class="sos-contacts-grid"><SosContactCard v-for="contact in emergencyContacts" :key="contact.title" v-bind="contact" /></div></div></section>
    <section class="sos-docs-section"><div class="sos-inner"><div class="sos-section-header"><h2>Шаблоны документов</h2><p>Готовые формы для официальных обращений</p></div><div class="sos-docs-grid"><article v-for="doc in documents" :key="doc.title" class="sos-doc-card"><div class="sos-icon-wrap light"><MdiIcon :path="doc.icon" :size="28" /></div><div><h3>{{ doc.title }}</h3><p>{{ doc.text }}</p></div><a :href="doc.url" download><MdiIcon :path="mdiDownload" :size="18" />Скачать</a></article></div></div></section>
    <section class="sos-agent-section"><div class="sos-inner sos-agent-grid"><div class="sos-agent-copy"><h2>ИИ-помощник рядом 24/7</h2><p>Опишите ситуацию простыми словами. Помощник предложит первые безопасные шаги.</p><ul><li>Пошаговая инструкция действий</li><li>Подсказка, куда обратиться</li><li>Помощь в составлении обращения</li></ul></div><div class="sos-chat"><div class="sos-chat-header"><div class="sos-bot-avatar"><MdiIcon :path="mdiRobotOutline" :size="22" /></div><div><b>ИИ-агент</b><span>Онлайн 24/7</span></div></div><div class="sos-messages"><div v-for="(message,index) in messages" :key="index" class="sos-message-row" :class="message.role"><div class="sos-bubble">{{ message.text }}</div><small>{{ message.time }}</small></div><div v-if="loading" class="sos-message-row agent"><div class="sos-bubble">Печатает...</div></div></div><div class="sos-input-row"><input v-model="input" placeholder="Опишите свою ситуацию" @keydown.enter.prevent="send"><button :disabled="!input.trim()" @click="send"><MdiIcon :path="mdiSend" :size="20" /></button></div></div></div></section>
  </div>
</template>
