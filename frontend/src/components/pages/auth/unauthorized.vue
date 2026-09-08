<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseButton from '../../UI/BaseButton.vue'
import BaseCard from '../../UI/BaseCard.vue'
import ThemeToggle from '../../UI/ThemeToggle.vue'
import { useAuth } from '../../../composables/useAuth'

const router = useRouter()
const { user, logout } = useAuth()

async function signOut() {
  await logout()
  await router.replace('/login')
}
</script>

<template>
  <main class="relative flex min-h-screen items-center justify-center bg-paper px-4 py-16">
    <div class="absolute right-4 top-4"><ThemeToggle /></div>
    <BaseCard class="w-full max-w-lg text-center" padding="lg">
      <div class="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-full bg-accent/10 text-accent">
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16.5 10.5V6.75a4.5 4.5 0 00-9 0v3.75m-.75 0h10.5a1.5 1.5 0 011.5 1.5v7.5h-13.5V12a1.5 1.5 0 011.5-1.5z"/></svg>
      </div>
      <p class="mb-3 text-xs font-semibold uppercase tracking-[.16em] text-accent">Acceso restringido</p>
      <h1 class="text-3xl sm:text-4xl">Esta cuenta no tiene permisos</h1>
      <p class="mx-auto mt-4 text-ink-2">
        <strong class="font-medium text-ink">{{ user?.email }}</strong> inició sesión correctamente, pero no está habilitada para administrar el catálogo.
      </p>
      <div class="mt-8 flex flex-col-reverse justify-center gap-2 sm:flex-row">
        <router-link to="/"><BaseButton variant="ghost" class="w-full">Volver al sitio</BaseButton></router-link>
        <BaseButton @click="signOut">Usar otra cuenta</BaseButton>
      </div>
    </BaseCard>
  </main>
</template>
