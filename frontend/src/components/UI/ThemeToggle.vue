<script setup lang="ts">
import { useTheme } from '../../composables/useTheme'
defineProps<{ inverted?: boolean }>()
const { isDark } = useTheme()
</script>

<template>
  <button
    type="button"
    disabled
    aria-disabled="true"
    aria-label="Cambio de tema temporalmente deshabilitado"
    title="Cambio de tema temporalmente deshabilitado"
    :class="[
      'inline-flex min-h-11 min-w-11 cursor-not-allowed items-center justify-center rounded-[var(--radius-md)] opacity-45',
      inverted ? 'text-[#E3D5C1]/80' : 'text-accent'
    ]"
  >
    <svg v-if="isDark" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3v2m0 14v2M3 12h2m14 0h2m-3.64-6.36-1.42 1.42M8.06 15.94l-1.42 1.42m0-11.72 1.42 1.42m7.88 8.88 1.42 1.42M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
    <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M20.3 15.3A9 9 0 118.7 3.7 7 7 0 0020.3 15.3z" /></svg>
  </button>
</template>
