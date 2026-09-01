<script setup lang="ts">
import BaseModal from '../UI/BaseModal.vue'
import BaseButton from '../UI/BaseButton.vue'
import type { Author } from '../../types/domain'

defineProps<{
  open: boolean
  author: Author | null
}>()

const emit = defineEmits<{
  close: []
}>()
</script>

<template>
  <BaseModal
    :open="open"
    title="Información del autor"
    max-width="lg"
    @close="emit('close')"
  >
    <div v-if="author" class="flex flex-col gap-4">
      <div>
        <p class="text-xs font-[var(--font-mono)] text-accent tracking-wide uppercase mb-1">
          {{ author.country }} · {{ author.birth_year }}–{{ author.death_year || 'presente' }}
        </p>
        <h2 class="text-2xl font-[var(--font-display)]">{{ author.name }}</h2>
      </div>

      <div class="h-px bg-rule"></div>

      <div v-if="author.biography">
        <p class="text-ink-3 mb-1 text-sm">Biografía</p>
        <p class="text-ink leading-relaxed">{{ author.biography }}</p>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end">
        <BaseButton variant="ghost" size="sm" @click="emit('close')">Cerrar</BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
