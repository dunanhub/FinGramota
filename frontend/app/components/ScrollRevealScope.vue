<script setup lang="ts">
const route = useRoute()
const root = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | undefined
let mutationObserver: MutationObserver | undefined

const cardSelector = [
  '.mp-tip', '.mp-bank', '.courses-grid > *', '.popular-grid > *',
  '.tools-grid > *', '.sos-contacts-grid > *', '.sos-docs-grid > *',
  '.trainer-grid > *', '.game-map-inner > *', '.profile-card', '.faq-accordion'
].join(',')

function setupReveal() {
  if (!root.value) return
  observer?.disconnect()

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const sections = Array.from(root.value.querySelectorAll<HTMLElement>('section'))
  const cards = Array.from(root.value.querySelectorAll<HTMLElement>(cardSelector))
  const targets = [...new Set([...sections, ...cards])]

  targets.forEach((element, index) => {
    element.classList.add('site-reveal')
    if (cards.includes(element)) element.style.setProperty('--reveal-delay', `${(index % 6) * 80}ms`)
    if (reducedMotion) element.classList.add('site-reveal--visible')
  })

  if (reducedMotion) return
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return
      entry.target.classList.add('site-reveal--visible')
      observer?.unobserve(entry.target)
    })
  }, { threshold: 0.1, rootMargin: '0px 0px -7%' })
  targets.forEach(element => observer?.observe(element))
}

onMounted(() => {
  requestAnimationFrame(setupReveal)
  mutationObserver = new MutationObserver(() => requestAnimationFrame(setupReveal))
  if (root.value) mutationObserver.observe(root.value, { childList: true, subtree: true })
})

watch(() => route.fullPath, () => nextTick(() => requestAnimationFrame(setupReveal)))

onBeforeUnmount(() => {
  observer?.disconnect()
  mutationObserver?.disconnect()
})
</script>

<template>
  <div ref="root" class="scroll-reveal-scope"><slot /></div>
</template>
