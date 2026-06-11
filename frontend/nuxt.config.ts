import tailwindcss from '@tailwindcss/vite'

const runtimeEnv = (globalThis as {
  process?: { env?: Record<string, string | undefined> }
}).process?.env ?? {}

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
    server: {
      watch: {
        usePolling: runtimeEnv.CHOKIDAR_USEPOLLING === 'true',
        interval: Number(runtimeEnv.CHOKIDAR_INTERVAL || 300),
        ignored: ['**/node_modules/**', '**/.nuxt/**', '**/.output/**']
      },
      hmr: {
        clientPort: 3000
      }
    }
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: 'http://localhost:8000'
    }
  },
  app: {
    head: {
      htmlAttrs: { lang: 'ru' },
      title: 'FinGramota',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  }
})
