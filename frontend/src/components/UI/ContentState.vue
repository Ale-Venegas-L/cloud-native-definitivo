<script setup lang="ts">
defineProps<{ title: string; description?: string; tone?: 'neutral' | 'error'; retryable?: boolean }>()
defineEmits<{ retry: [] }>()
</script>

<template>
  <div class="rounded-[var(--radius-lg)] border border-dashed border-rule bg-paper-2/40 px-6 py-12 text-center" role="status">
    <div :class="['mx-auto mb-4 flex h-11 w-11 items-center justify-center rounded-full', tone === 'error' ? 'bg-danger/10 text-danger' : 'bg-paper-3 text-ink-3']"><svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 4.5h.008v.008H12V16.5z" /></svg></div>
    <h3 class="text-xl">{{ title }}</h3>
    <p v-if="description" class="mx-auto mt-2 text-sm text-ink-3">{{ description }}</p>
    <button v-if="retryable" type="button" class="mt-5 min-h-11 rounded-md border border-rule px-4 text-sm font-medium text-ink hover:bg-paper-2" @click="$emit('retry')">Reintentar</button>
  </div>
</template>
