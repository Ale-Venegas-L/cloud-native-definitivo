<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { handleCallback } from '../../../composables/useAuth'

const route = useRoute()
const router = useRouter()
const error = ref('')

onMounted(async () => {
  const code = route.query.code as string | undefined
  const stateParam = route.query.state as string | undefined

  if (!code || !stateParam) {
    error.value = 'Parámetros de autorización faltantes'
    return
  }

  const success = await handleCallback(code, stateParam)

  if (success) {
    const redirect = route.query.redirect as string
    await router.replace(redirect || '/admin')
  } else {
    error.value = 'Error al procesar la autorización'
  }
})
</script>

<template>
  <main class="flex min-h-screen items-center justify-center bg-paper">
    <div class="text-center">
      <div v-if="!error" class="flex flex-col items-center gap-4">
        <div class="h-8 w-8 animate-spin rounded-full border-2 border-accent border-t-transparent" />
        <p class="text-ink-2">Procesando autenticación…</p>
      </div>
      <div v-else class="flex flex-col items-center gap-4">
        <p class="text-danger">{{ error }}</p>
        <router-link to="/login" class="text-sm text-accent hover:underline">Volver al login</router-link>
      </div>
    </div>
  </main>
</template>
