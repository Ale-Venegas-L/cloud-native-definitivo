<script setup lang="ts">
import { computed } from 'vue'
import BaseModal from '../UI/BaseModal.vue'
import BaseButton from '../UI/BaseButton.vue'
import BookArtwork from '../UI/BookArtwork.vue'
import type { Author, Book } from '../../types/domain'
import { editionForBook } from '../../data/editions'

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
const edition = computed(() => props.book ? editionForBook(props.book.title) : undefined)

function getAuthorName(id: string): string {
  return props.authors.find(a => a.id === id)?.name || '—'
}
</script>

<template>
  <BaseModal
    :open="open"
    :title="isEditing ? 'Detalle del libro' : 'Información del libro'"
    max-width="xl"
    @close="emit('close')"
  >
    <div v-if="book" class="grid gap-6 sm:grid-cols-[minmax(0,13rem)_1fr]">
      <div><BookArtwork :book="book" eager sizes="208px"/><p v-if="edition" class="mt-3 text-center font-[var(--font-mono)] text-[.62rem] uppercase tracking-wider text-ink-3">{{ edition.kind }} · {{ edition.year }}</p></div>
      <div class="flex min-w-0 flex-col gap-4"><div><p class="mb-1 font-[var(--font-mono)] text-xs uppercase tracking-wide text-accent">{{ book.genre }} · {{ book.publication_year }}</p><h2 class="text-2xl sm:text-3xl">{{ book.title }}</h2></div><div class="h-px bg-rule"/><div class="grid grid-cols-2 gap-4 text-sm"><div><p class="mb-1 text-ink-3">Autor</p><p class="font-medium text-ink">{{ getAuthorName(book.author_id) }}</p></div><div><p class="mb-1 text-ink-3">País</p><p class="font-medium text-ink">{{ book.country }}</p></div></div><div v-if="book.description"><p class="mb-1 text-sm text-ink-3">Descripción</p><p class="leading-relaxed text-ink">{{ book.description }}</p></div><p v-if="edition" class="mt-auto border-t border-rule pt-3 text-xs leading-relaxed text-ink-3">{{ edition.description }}</p></div>
    </div>

    <template #footer>
      <div class="flex justify-end">
        <BaseButton variant="ghost" size="sm" @click="emit('close')">Cerrar</BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
