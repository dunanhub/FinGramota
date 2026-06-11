<script setup lang="ts">
import {
  mdiAlertOutline,
  mdiChartLineVariant,
  mdiCurrencyUsd,
  mdiShieldCheckOutline
} from '@mdi/js'

const benefits = [
  { icon: mdiCurrencyUsd, title: 'Изучать финансы простым языком', desc: 'Курсы и материалы для повседневной финансовой грамотности.' },
  { icon: mdiShieldCheckOutline, title: 'Проверять финансовые организации', desc: 'Быстрая проверка лицензий, сайтов и инвестиционных проектов.' },
  { icon: mdiAlertOutline, title: 'Избегать мошенничества', desc: 'Узнавайте признаки финансовых пирамид и подозрительных схем.' },
  { icon: mdiChartLineVariant, title: 'Развивать финансовые навыки', desc: 'Учитесь управлять бюджетом, накоплениями и личными финансами.' }
]

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  password: '',
  confirm: '',
  agree: false
})

const rules = computed(() => [
  { label: 'Минимум 8 символов', ok: form.password.length >= 8 },
  { label: 'Содержит цифры и буквы', ok: /[0-9]/.test(form.password) && /[a-zA-Zа-яА-Я]/.test(form.password) },
  { label: 'Минимум одна заглавная буква', ok: /[A-ZА-Я]/.test(form.password) }
])

function submit() {
  navigateTo('/home')
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-logo">
      <img src="/logo.svg" alt="FinGramota">
    </div>
    <div class="auth-card auth-card--wide">
      <div class="auth-form-col">
        <h1 class="auth-title"><span class="auth-title__bar" />Создайте аккаунт</h1>
        <p class="auth-desc">Получите доступ к обучению, проверке финансовых организаций и полезным инструментам финансовой грамотности.</p>
        <form class="auth-form" @submit.prevent="submit">
          <div class="auth-field"><label class="auth-label" for="reg-first">Имя</label><input id="reg-first" v-model="form.firstName" class="auth-input" placeholder="Введите ваше имя"></div>
          <div class="auth-field"><label class="auth-label" for="reg-last">Фамилия</label><input id="reg-last" v-model="form.lastName" class="auth-input" placeholder="Введите вашу фамилию"></div>
          <div class="auth-field"><label class="auth-label" for="reg-email">Почта</label><input id="reg-email" v-model="form.email" class="auth-input" type="email" placeholder="Введите ваш email"></div>
          <div class="auth-field"><label class="auth-label" for="reg-phone">Телефон</label><input id="reg-phone" v-model="form.phone" class="auth-input" type="tel" placeholder="+7 (___) ___ __ __"></div>
          <div class="auth-field">
            <label class="auth-label" for="reg-pass">Пароль</label>
            <AuthPasswordField id="reg-pass" v-model="form.password" placeholder="Введите пароль" autocomplete="new-password" />
            <ul class="auth-rules">
              <li v-for="rule in rules" :key="rule.label" class="auth-rule" :class="{ 'auth-rule--ok': rule.ok }"><span class="auth-rule__dot" />{{ rule.label }}</li>
            </ul>
          </div>
          <div class="auth-field"><label class="auth-label" for="reg-confirm">Подтвердите пароль</label><AuthPasswordField id="reg-confirm" v-model="form.confirm" placeholder="Повторите пароль" autocomplete="new-password" /></div>
          <label class="auth-checkbox">
            <input v-model="form.agree" type="checkbox"><span class="auth-checkbox__box" />
            <span class="auth-checkbox__text">Я согласен с условиями <a href="#" class="auth-link">Пользовательского соглашения</a> и <a href="#" class="auth-link">Политикой конфиденциальности</a></span>
          </label>
          <button class="auth-submit" type="submit" :disabled="!form.agree">Зарегистрироваться</button>
          <p class="auth-switch">Уже есть аккаунт? <NuxtLink to="/login" class="auth-link auth-link--gold">Войти</NuxtLink></p>
        </form>
      </div>
      <div class="auth-benefits-col">
        <h2 class="auth-benefits-title">С FinGramota<br><span class="auth-benefits-title__gold">вы получаете</span></h2>
        <ul class="auth-benefits">
          <li v-for="benefit in benefits" :key="benefit.title" class="auth-benefit">
            <div class="auth-benefit__icon"><MdiIcon :path="benefit.icon" :size="26" /></div>
            <div><p class="auth-benefit__title">{{ benefit.title }}</p><p class="auth-benefit__desc">{{ benefit.desc }}</p></div>
          </li>
        </ul>
        <div class="auth-shield-placeholder"><img src="/14-shield.svg" alt="" class="auth-shield-img"></div>
      </div>
    </div>
  </div>
</template>
