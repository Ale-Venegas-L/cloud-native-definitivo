<script setup lang="ts">
import { computed } from 'vue'
import BaseModal from '../UI/BaseModal.vue'
import BaseButton from '../UI/BaseButton.vue'

interface Book {
  title: string
  author_id: string
  country: string
  publication_year: number
  genre: string
  description?: string
}

interface Author {
  id: string
  name: string
}

const props = defineProps<{
  open: boolean
  book: Book | null
  authors: Author[]
}>()

const emit = defineEmits<{
  close: []
  save: [data: Book]
}>()

const isEditing = computed(() => !!props.book)

function getAuthorName(id: string): string {
  return props.authors.find(a => a.id === id)?.name || '—'
}
</script>

<template>
  <BaseModal
    :open="open"
    :title="isEditing ? 'Detalle del libro' : 'Información del libro'"
    max-width="lg"
    @close="emit('close')"
  >
    <div v-if="book" class="flex flex-col gap-4">
      <div>
        <p class="text-xs font-[var(--font-mono)] text-accent tracking-wide uppercase mb-1">
          {{ book.genre }} · {{ book.publication_year }}
        </p>
        <h2 class="text-2xl font-[var(--font-display)]">{{ book.title }}</h2>
      </div>

      <div class="h-px bg-rule"></div>

      <div class="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p class="text-ink-3 mb-1">Autor</p>
          <p class="text-ink font-medium">{{ getAuthorName(book.author_id) }}</p>
        </div>
        <div>
          <p class="text-ink-3 mb-1">País</p>
          <p class="text-ink font-medium">{{ book.country }}</p>
        </div>
      </div>

      <div v-if="book.description">
        <p class="text-ink-3 mb-1 text-sm">Descripción</p>
        <p class="text-ink leading-relaxed">{{ book.description }}</p>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end">
        <BaseButton variant="ghost" size="sm" @click="emit('close')">Cerrar</BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
