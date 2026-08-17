<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const mobileOpen = ref(false)

const navLinks = [
  { label: 'Inicio', to: '/' },
  { label: 'Catálogo', to: '/books' },
  { label: 'Admin', to: '/admin' }
]
</script>

<template>
  <header class="sticky top-0 z-[var(--z-sticky)] bg-paper/80 backdrop-blur-md border-b border-rule">
    <nav class="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between">
      <router-link
        to="/"
        class="font-[var(--font-display)] text-2xl text-ink tracking-tight hover:text-accent transition-colors duration-[var(--dur-short)]"
      >
        Classic Library
      </router-link>

      <div class="hidden md:flex items-center gap-8">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          :class="[
            'text-sm font-medium transition-colors duration-[var(--dur-short)]',
            route.path === link.to || (link.to !== '/' && route.path.startsWith(link.to))
              ? 'text-accent'
              : 'text-ink-2 hover:text-ink'
          ]"
        >
          {{ link.label }}
        </router-link>
      </div>

      <button
        class="md:hidden p-2 text-ink-2 hover:text-ink transition-colors"
        @click="mobileOpen = !mobileOpen"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </nav>

    <div v-if="mobileOpen" class="md:hidden border-t border-rule bg-paper">
      <div class="px-5 py-3 flex flex-col gap-2">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          :class="[
            'px-3 py-2 rounded-[var(--radius-md)] text-sm font-medium transition-colors',
            route.path === link.to || (link.to !== '/' && route.path.startsWith(link.to))
              ? 'bg-accent/10 text-accent'
              : 'text-ink-2 hover:bg-paper-2'
          ]"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </router-link>
      </div>
    </div>
  </header>
</template>
