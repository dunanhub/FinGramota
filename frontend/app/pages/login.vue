<script setup lang="ts">
const form = reactive({ login: '', password: '', remember: false })
</script>

<template>
  <div class="auth-page">
    <div class="auth-logo">
      <div class="auth-logo__icon"><img src="/logo_1.svg" alt="" width="44" height="44"></div>
      <div><div class="auth-logo__name"><span class="auth-logo__fin">Fin</span>Gramota</div><div class="auth-logo__sub">ГОСУДАРСТВЕННАЯ ПЛАТФОРМА</div></div>
    </div>
    <div class="auth-card auth-card--narrow">
      <h1 class="auth-title"><span class="auth-title__bar" />Вход в аккаунт</h1>
      <p class="auth-desc">Получите доступ к обучению, проверке финансовых организаций и полезным инструментам финансовой грамотности.</p>
      <form class="auth-form" @submit.prevent="navigateTo('/home')">
        <div class="auth-field"><label class="auth-label" for="login-email">Логин/email</label><input id="login-email" v-model="form.login" class="auth-input" placeholder="Введите ваш логин/email" autocomplete="username"></div>
        <div class="auth-field"><label class="auth-label" for="login-pass">Пароль</label><AuthPasswordField id="login-pass" v-model="form.password" placeholder="Введите пароль" /></div>
        <div class="auth-row-between">
          <label class="auth-checkbox"><input v-model="form.remember" type="checkbox"><span class="auth-checkbox__box" /><span class="auth-checkbox__text">Запомнить меня</span></label>
          <a href="#" class="auth-link auth-link--muted">Забыли пароль?</a>
        </div>
        <button class="auth-submit" type="submit" :disabled="!form.login.trim() || !form.password.trim()">Войти</button>
        <p class="auth-switch">Нет аккаунта? <NuxtLink to="/register" class="auth-link auth-link--gold">Зарегистрироваться</NuxtLink></p>
      </form>
    </div>
  </div>
</template>
