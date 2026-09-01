import { computed, ref } from 'vue'

type Theme = 'light' | 'dark'
export const THEME_SWITCHING_ENABLED = false
const theme = ref<Theme>('light')
let initialized = false

function isTheme(value: string | undefined | null): value is Theme {
  return value === 'light' || value === 'dark'
}

function applyTheme(nextTheme: Theme): void {
  document.documentElement.dataset.theme = nextTheme
}

export function initializeTheme(): void {
  if (initialized || typeof window === 'undefined') return
  if (!THEME_SWITCHING_ENABLED) {
    theme.value = 'light'
    applyTheme(theme.value)
    initialized = true
    return
  }
  const stored = window.localStorage.getItem('classic-library-theme') as Theme | null
  const preferred = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  const preloaded = document.documentElement.dataset.theme
  theme.value = isTheme(preloaded) ? preloaded : isTheme(stored) ? stored : preferred
  applyTheme(theme.value)
  initialized = true
}

export function useTheme() {
  initializeTheme()
  function toggleTheme(): void {
    if (!THEME_SWITCHING_ENABLED) return
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    applyTheme(theme.value)
    window.localStorage.setItem('classic-library-theme', theme.value)
  }
  return { theme: computed(() => theme.value), isDark: computed(() => theme.value === 'dark'), toggleTheme }
}
