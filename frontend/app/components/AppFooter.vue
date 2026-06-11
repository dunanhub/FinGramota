<script setup lang="ts">
import {
  mdiEmailOutline,
  mdiFacebook,
  mdiInstagram,
  mdiMapMarkerOutline,
  mdiPhoneOutline,
  mdiTwitter,
  mdiYoutube
} from '@mdi/js'
</script>

<template>
  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-top">
        <div class="footer-brand">
          <img src="/logo.svg" alt="FinGramota">
          <p>Ваш надежный проводник в мире финансов. Помогаем принимать осознанные решения и защищаем от мошенников.</p>
          <div class="socials">
            <MdiIcon :path="mdiFacebook" :size="19" />
            <MdiIcon :path="mdiInstagram" :size="19" />
            <MdiIcon :path="mdiTwitter" :size="19" />
            <MdiIcon :path="mdiYoutube" :size="19" />
          </div>
        </div>
        <div class="footer-column">
          <h4>Платформа</h4>
          <a href="#">Вакансии</a><a href="#">Партнёры</a><a href="#">О проекте</a><a href="#">Новости</a>
        </div>
        <div class="footer-column">
          <h4>Инструменты</h4>
          <NuxtLink to="/marketplace#calculator">Кредитный калькулятор</NuxtLink>
          <NuxtLink to="/check">Проверка брокера</NuxtLink>
          <NuxtLink to="/sos">Сообщить о мошенничестве</NuxtLink>
          <NuxtLink to="/faq">Финансовый словарь</NuxtLink>
        </div>
        <div class="footer-column contacts">
          <h4>Контакты</h4>
          <p><MdiIcon :path="mdiMapMarkerOutline" :size="22" /><span>г. Астана, пр. Мангилик Ел, 55А, БЦ «Байтерек»</span></p>
          <p class="phone"><MdiIcon :path="mdiPhoneOutline" :size="22" /><strong>1459 (Call-center)</strong></p>
          <p><MdiIcon :path="mdiEmailOutline" :size="22" /><span>info@fingramota.kz</span></p>
        </div>
      </div>
      <div class="footer-bottom">
        <a href="#">Политика конфиденциальности</a>
        <span>© 2026 FinGramota. Все права защищены.</span>
        <a href="#">Условия использования</a>
      </div>
    </div>
  </footer>
</template>
