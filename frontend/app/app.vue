<script setup lang="ts">
const route = useRoute()
const layoutName = computed(() => ['/', '/register', '/login'].includes(route.path) ? 'auth' : 'default')
</script>

<template>
  <NuxtRouteAnnouncer />
  <NuxtLayout :name="layoutName">
    <NuxtPage />
  </NuxtLayout>
</template>
