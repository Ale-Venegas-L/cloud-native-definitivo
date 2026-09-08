<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import BaseButton from '../../UI/BaseButton.vue'
import ThemeToggle from '../../UI/ThemeToggle.vue'
import { useAuth } from '../../../composables/useAuth'

const route = useRoute()
const { loginWithCognito } = useAuth()
const isLoading = ref(false)
const errorMessage = ref('')

async function login() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    if (route.query.redirect) {
      sessionStorage.setItem('auth_redirect', route.query.redirect as string)
    }
    await loginWithCognito()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No fue posible iniciar sesión'
    isLoading.value = false
  }
}
</script>

<template>
  <main class="grid min-h-screen bg-paper lg:grid-cols-2">
    <section class="relative hidden overflow-hidden border-r border-[#E3D5C1]/15 bg-[#6C4A3C] p-12 text-[#E3D5C1] lg:flex lg:flex-col lg:justify-between">
      <router-link to="/" class="relative z-10 font-[var(--font-display)] text-2xl text-[#E3D5C1]">Classic Library</router-link>
      <div class="relative z-10 max-w-lg"><p class="mb-5 text-xs font-semibold uppercase tracking-[.18em] text-accent">Archivo administrativo</p><h1 class="text-[4.5rem] leading-[.95] text-[#E3D5C1]">Cuidar una colección también es contar su historia.</h1><p class="mt-6 text-[#E3D5C1]/70">Gestiona obras y autores desde un espacio seguro y diseñado para trabajar con claridad.</p></div>
      <div class="absolute -bottom-28 -right-24 h-96 w-96 rounded-full border border-[#E3D5C1]/10"/><div class="absolute -bottom-10 -right-4 h-64 w-64 rounded-full border border-[#E3D5C1]/10"/>
    </section>
    <section class="relative flex items-center justify-center px-5 py-16 sm:px-10"><div class="absolute right-4 top-4"><ThemeToggle /></div><div class="w-full max-w-md">
      <router-link to="/" class="mb-12 inline-block font-[var(--font-display)] text-2xl text-ink lg:hidden">Classic Library</router-link>
      <p class="mb-3 text-xs font-semibold uppercase tracking-[.16em] text-accent">Administración</p><h1 class="text-4xl sm:text-5xl">Bienvenido</h1><p class="mt-4 text-ink-2">Accede con la cuenta autorizada para administrar la biblioteca.</p>
      <div v-if="errorMessage" class="mt-6 rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger" role="alert">{{ errorMessage }}</div>
      <BaseButton class="mt-8 w-full" :loading="isLoading" @click="login">
        <svg v-if="!isLoading" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3" />
        </svg>
        {{ isLoading ? 'Conectando de forma segura…' : 'Iniciar sesión' }}
      </BaseButton>
      <div class="mt-6 flex items-center gap-2 text-xs text-ink-3">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16.5 10.5V6.75a4.5 4.5 0 00-9 0v3.75m-.75 0h10.5a1.5 1.5 0 011.5 1.5v7.5h-13.5V12a1.5 1.5 0 011.5-1.5z"/></svg>
        Autenticación segura con AWS Cognito.
      </div>
      <router-link to="/" class="mt-10 inline-flex min-h-11 items-center text-sm text-ink-3 hover:text-accent">← Volver al sitio público</router-link>
    </div></section>
  </main>
</template>
