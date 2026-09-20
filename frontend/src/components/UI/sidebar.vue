<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import ThemeToggle from './ThemeToggle.vue'

defineProps<{ open: boolean }>()
const emit = defineEmits<{ close: [] }>()
const route = useRoute()
const router = useRouter()
const { user, logout } = useAuth()
const links = [
  { label: 'Dashboard', to: '/admin', icon: 'grid' },
  { label: 'Biblioteca', to: '/admin/stock', icon: 'book' },
  { label: 'Volver al sitio', to: '/', icon: 'external' }
]
async function signOut() { await logout(); await router.replace('/') }
</script>

<template>
  <button v-if="open" type="button" class="fixed inset-0 z-[190] bg-backdrop lg:hidden" aria-label="Cerrar menú" @click="emit('close')" />
  <aside :class="['fixed inset-y-0 left-0 z-[var(--z-sticky)] flex w-72 flex-col border-r border-rule bg-paper-2 transition-transform duration-[var(--dur-long)] lg:w-64 lg:translate-x-0', open ? 'translate-x-0' : '-translate-x-full']" aria-label="Navegación administrativa">
    <div class="flex min-h-16 items-center justify-between border-b border-rule px-5">
      <router-link to="/admin" class="font-[var(--font-display)] text-xl text-ink" @click="emit('close')">Classic Library <span class="text-accent">Admin</span></router-link>
      <button type="button" class="inline-flex min-h-11 min-w-11 items-center justify-center text-ink-3 lg:hidden" aria-label="Cerrar menú" @click="emit('close')"><span class="text-2xl">×</span></button>
    </div>
    <nav class="flex flex-1 flex-col gap-1 px-3 py-4">
      <router-link v-for="link in links" :key="link.to" :to="link.to" :class="['flex min-h-11 items-center gap-3 rounded-md px-3 text-sm font-medium transition-colors', route.path === link.to || (link.to !== '/admin' && link.to !== '/' && route.path.startsWith(link.to)) ? 'bg-accent/10 text-accent' : 'text-ink-2 hover:bg-paper-3 hover:text-ink']" @click="emit('close')">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path v-if="link.icon === 'grid'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/><path v-else-if="link.icon === 'book'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.25v13m0-13C10.8 5.5 9.2 5 7.5 5S4.2 5.5 3 6.25v13C4.2 18.5 5.8 18 7.5 18s3.3.5 4.5 1.25m0-13C13.2 5.5 14.8 5 16.5 5s3.3.5 4.5 1.25v13C19.8 18.5 18.2 18 16.5 18s-3.3.5-4.5 1.25"/><path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        {{ link.label }}
      </router-link>
    </nav>
    <div class="border-t border-rule px-4 py-4">
      <div class="flex items-center gap-3">
        <img v-if="user?.picture" :src="user.picture" alt="" class="h-9 w-9 rounded-full" referrerpolicy="no-referrer">
        <div class="min-w-0 flex-1"><p class="truncate text-sm font-medium text-ink">{{ user?.name || 'Administrador' }}</p><p class="truncate text-xs text-ink-3">{{ user?.email }}</p></div>
        <ThemeToggle />
      </div>
      <button type="button" class="mt-3 min-h-11 w-full rounded-md border border-rule text-sm font-medium text-ink-2 hover:bg-paper-3" @click="signOut">Cerrar sesión</button>
    </div>
  </aside>
</template>
