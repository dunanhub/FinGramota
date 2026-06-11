export interface ChatMessage {
  role: 'user' | 'agent'
  text: string
  time?: string
}

export interface HomeItem {
  title: string
  image: string
  date?: string
}

const fallbackNews: HomeItem[] = Array.from({ length: 8 }, (_, index) => ({
  title: 'Банкротство физических лиц в Казахстане: как работает и кому это нужно',
  date: '09.04.2026',
  image: `/news/news-${(index % 3) + 1}.svg`
}))

const fallbackPodcasts: HomeItem[] = Array.from({ length: 6 }, () => ({
  title: 'Цифровые информационные ресурсы',
  image: '/podcasts/podcast-1.svg'
}))

export function useFinGramotaApi() {
  const config = useRuntimeConfig()
  const apiBase = String(config.public.apiBaseUrl || '').replace(/\/$/, '')

  async function getHomeContent() {
    try {
      const data = await $fetch<{ news?: HomeItem[], podcasts?: HomeItem[] }>(`${apiBase}/api/home-content`)
      return {
        news: data.news?.length ? data.news : fallbackNews,
        podcasts: data.podcasts?.length ? data.podcasts : fallbackPodcasts
      }
    } catch {
      return { news: fallbackNews, podcasts: fallbackPodcasts }
    }
  }

  async function sendAgentMessage(messages: ChatMessage[]) {
    const payload = messages.map(message => ({
      role: message.role === 'agent' ? 'assistant' : 'user',
      content: message.text
    }))
    const data = await $fetch<{ text: string }>(`${apiBase}/api/agent/chat`, {
      method: 'POST',
      body: { messages: payload }
    })
    return data.text
  }

  async function downloadTemplate(filename: string) {
    return $fetch<Blob>(`${apiBase}/api/documents/${encodeURIComponent(filename)}`, {
      responseType: 'blob'
    })
  }

  return { getHomeContent, sendAgentMessage, downloadTemplate }
}
