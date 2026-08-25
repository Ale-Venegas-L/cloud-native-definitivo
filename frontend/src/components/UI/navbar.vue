<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import ThemeToggle from './ThemeToggle.vue'

const route = useRoute()
const mobileOpen = ref(false)
const isScrolled = ref(false)
const { isAdmin, isAuthenticated } = useAuth()
const navLinks = computed(() => [
  { label: 'Inicio', to: '/' },
  { label: 'Catálogo', to: '/books' },
  { label: 'Ediciones', to: '/editions' },
  isAdmin.value ? { label: 'Administración', to: '/admin' } : isAuthenticated.value ? { label: 'Sin acceso', to: '/unauthorized' } : { label: 'Ingresar', to: '/login' }
])
const isTransparent = computed(() => route.name === 'home' && !isScrolled.value && !mobileOpen.value)

function updateScrollState() { isScrolled.value = window.scrollY > 16 }
onMounted(() => { updateScrollState(); window.addEventListener('scroll', updateScrollState, { passive: true }) })
onBeforeUnmount(() => window.removeEventListener('scroll', updateScrollState))

watch(() => route.fullPath, () => { mobileOpen.value = false })
</script>

<template>
  <header :class="['fixed inset-x-0 top-0 z-[var(--z-sticky)] transition-[background-color,border-color,box-shadow] duration-[var(--dur-short)]', isTransparent ? 'border-b border-transparent bg-transparent' : 'border-b border-rule bg-paper/90 shadow-[var(--shadow-whisper)] backdrop-blur-md']">
    <nav class="page-shell flex h-16 items-center justify-between" aria-label="Navegación principal">
      <router-link to="/" :class="['font-[var(--font-display)] text-2xl tracking-tight transition-colors', isTransparent ? 'text-[#E3D5C1] hover:text-[#E3D5C1]' : 'text-accent hover:text-accent-2']">Classic Library</router-link>
      <div class="hidden items-center gap-1 md:flex">
        <router-link v-for="link in navLinks" :key="link.to" :to="link.to" :class="['flex min-h-11 items-center rounded-md px-4 text-sm font-medium transition-colors', route.path === link.to || (link.to !== '/' && route.path.startsWith(link.to)) ? (isTransparent ? 'bg-[#E3D5C1]/10 text-[#E3D5C1]' : 'bg-accent/10 text-accent') : (isTransparent ? 'text-[#E3D5C1]/80 hover:bg-[#E3D5C1]/10 hover:text-[#E3D5C1]' : 'text-accent hover:bg-paper-2 hover:text-accent-2')]">{{ link.label }}</router-link>
        <ThemeToggle :inverted="isTransparent" />
      </div>
      <div class="flex items-center md:hidden">
        <ThemeToggle :inverted="isTransparent" />
        <button type="button" :class="['inline-flex min-h-11 min-w-11 items-center justify-center', isTransparent ? 'text-[#E3D5C1]' : 'text-ink-2']" :aria-expanded="mobileOpen" aria-controls="mobile-navigation" :aria-label="mobileOpen ? 'Cerrar menú' : 'Abrir menú'" @click="mobileOpen = !mobileOpen">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /><path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>
    </nav>
    <div v-if="mobileOpen" id="mobile-navigation" class="border-t border-rule bg-paper md:hidden">
      <nav class="page-shell flex flex-col gap-1 py-3" aria-label="Navegación móvil">
        <router-link v-for="link in navLinks" :key="link.to" :to="link.to" :class="['flex min-h-11 items-center rounded-md px-3 text-sm font-medium', route.path === link.to || (link.to !== '/' && route.path.startsWith(link.to)) ? 'bg-accent/10 text-accent' : 'text-accent hover:bg-paper-2 hover:text-accent-2']">{{ link.label }}</router-link>
      </nav>
    </div>
  </header>
</template>
