export function useReveal(delay = 0) {
  const visible = ref(false)
  let timer: ReturnType<typeof setTimeout> | undefined

  onMounted(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      visible.value = true
      return
    }

    timer = setTimeout(() => {
      visible.value = true
    }, delay)
  })

  onBeforeUnmount(() => {
    if (timer) clearTimeout(timer)
  })

  const revealStyle = computed(() => ({
    opacity: visible.value ? 1 : 0,
    transform: visible.value ? 'translateY(0)' : 'translateY(24px)',
    transition: 'opacity 0.6s ease, transform 0.6s ease'
  }))

  return { visible, revealStyle }
}

export function useRevealOnScroll(threshold = 0.12, rootMargin = '0px 0px -8%') {
  const target = ref<HTMLElement | null>(null)
  const visible = ref(false)
  let observer: IntersectionObserver | undefined
  let mounted = false

  const observe = (element: HTMLElement) => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      visible.value = true
      return
    }

    if (element.id && window.location.hash === `#${element.id}`) {
      visible.value = true
      return
    }

    observer?.disconnect()
    observer = new IntersectionObserver(([entry]) => {
      if (entry?.isIntersecting) {
        visible.value = true
        observer?.disconnect()
      }
    }, { threshold, rootMargin })
    observer.observe(element)
  }

  onMounted(() => {
    mounted = true
    if (target.value) observe(target.value)
  })

  watch(target, (element) => {
    if (mounted && element && !visible.value) observe(element)
  }, { flush: 'post' })

  onBeforeUnmount(() => {
    mounted = false
    observer?.disconnect()
  })

  const revealStyle = computed(() => ({
    opacity: visible.value ? 1 : 0,
    transform: visible.value ? 'translateY(0)' : 'translateY(24px)'
  }))

  return { target, visible, revealStyle }
}
