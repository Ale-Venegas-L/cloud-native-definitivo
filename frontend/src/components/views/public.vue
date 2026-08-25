<script setup lang="ts">
import Navbar from '../UI/navbar.vue'
import Footer from '../UI/footer.vue'
</script>

<template>
  <div class="min-h-screen text-ink font-[var(--font-body)]">
    <a href="#main-content" class="fixed left-3 top-3 z-[500] -translate-y-20 rounded-md bg-ink px-4 py-2 text-sm text-paper focus:translate-y-0">Saltar al contenido</a>
    <Navbar />
    <main id="main-content" :class="$route.name === 'home' ? '' : 'pt-16'" tabindex="-1">
      <router-view />
    </main>
    <Footer />
  </div>
</template>
