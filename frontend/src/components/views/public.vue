<script setup lang="ts">
import Navbar from '../UI/navbar.vue'
import Footer from '../UI/footer.vue'
</script>

<template>
  <div class="min-h-screen bg-paper text-ink font-[var(--font-body)]">
    <Navbar />
    <main>
      <router-view />
    </main>
    <Footer />
  </div>
</template>
