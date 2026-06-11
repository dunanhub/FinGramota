<script setup lang="ts">
import { mdiAccountOutline, mdiMagnify, mdiWeb } from '@mdi/js'
import { navigation } from '../constants/navigation'

const route = useRoute()
</script>

<template>
  <header class="site-header">
    <div class="header-content">
      <NuxtLink to="/home" class="brand">
        <img src="/logo.svg" alt="FinGramota">
      </NuxtLink>

      <nav class="header-nav" aria-label="Основная навигация">
        <NuxtLink
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          :class="{ 'nav-link-active': route.path === item.to }"
        >
          {{ item.label }}
        </NuxtLink>
      </nav>

      <div class="header-actions">
        <button class="icon-btn" aria-label="Поиск">
          <MdiIcon :path="mdiMagnify" :size="25" />
        </button>
        <div class="lang">
          <MdiIcon :path="mdiWeb" :size="18" />
          <span>RU</span>
        </div>
        <NuxtLink to="/profile" class="cabinet-btn">
          <MdiIcon :path="mdiAccountOutline" :size="17" />
          <span>Личный кабинет</span>
        </NuxtLink>
      </div>
    </div>
  </header>
</template>
