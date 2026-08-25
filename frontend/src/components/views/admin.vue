<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '../UI/sidebar.vue'

const menuOpen = ref(false)
const route = useRoute()
watch(() => route.fullPath, () => { menuOpen.value = false })
</script>

<template>
  <div class="min-h-screen text-ink">
    <Sidebar :open="menuOpen" @close="menuOpen = false" />
    <header class="sticky top-0 z-[180] flex min-h-16 items-center justify-between border-b border-rule bg-paper/90 px-4 backdrop-blur lg:hidden">
      <button type="button" class="inline-flex min-h-11 min-w-11 items-center justify-center rounded-md text-ink-2 hover:bg-paper-2" aria-label="Abrir menú administrativo" @click="menuOpen = true"><svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg></button>
      <span class="font-[var(--font-display)] text-xl">Administración</span><span class="w-11" />
    </header>
    <main id="main-content" class="min-h-screen lg:ml-64"><div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8"><router-view /></div></main>
  </div>
</template>
