<script setup lang="ts">
import Sidebar from '../UI/sidebar.vue'
</script>

<template>
  <div class="min-h-screen bg-paper text-ink font-[var(--font-body)]">
    <Sidebar />
    <main class="ml-64 min-h-screen">
      <div class="px-8 py-8">
        <router-view />
      </div>
    </main>
  </div>
</template>
