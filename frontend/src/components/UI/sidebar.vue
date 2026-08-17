<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const sidebarLinks = [
  { label: 'Dashboard', to: '/admin', icon: 'grid' },
  { label: 'Libros', to: '/admin/stock', icon: 'book' },
  { label: 'Volver al sitio', to: '/', icon: 'external' }
]
</script>

<template>
  <aside class="fixed left-0 top-0 h-screen w-64 bg-paper-2 border-r border-rule z-[var(--z-sticky)] flex flex-col">
    <div class="px-5 py-5 border-b border-rule">
      <router-link to="/admin" class="font-[var(--font-display)] text-xl text-ink">
        Admin
      </router-link>
    </div>

    <nav class="flex-1 px-3 py-4 flex flex-col gap-1">
      <router-link
        v-for="link in sidebarLinks"
        :key="link.to"
        :to="link.to"
        :class="[
          'flex items-center gap-3 px-3 py-2.5 rounded-[var(--radius-md)] text-sm font-medium',
          'transition-colors duration-[var(--dur-short)]',
          route.path === link.to || (link.to !== '/admin' && route.path.startsWith(link.to) && link.to !== '/')
            ? 'bg-accent/10 text-accent'
            : 'text-ink-2 hover:bg-paper-3 hover:text-ink'
        ]"
      >
        <svg v-if="link.icon === 'grid'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
        </svg>
        <svg v-else-if="link.icon === 'book'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
        {{ link.label }}
      </router-link>
    </nav>

    <div class="px-5 py-4 border-t border-rule">
      <p class="text-xs text-ink-3">Classic Library v0.1</p>
    </div>
  </aside>
</template>
