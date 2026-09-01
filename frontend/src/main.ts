import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { initializeAuth } from './composables/useAuth'
import { initializeTheme } from './composables/useTheme'
import './style.css'

async function bootstrap() {
  initializeTheme()
  await initializeAuth()
  createApp(App).use(router).mount('#app')
}

bootstrap()
