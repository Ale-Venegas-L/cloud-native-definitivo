<script setup lang="ts">
import { computed } from 'vue'
import type { Book } from '../../types/domain'
import { editionForBook } from '../../data/editions'
import BookCover from './BookCover.vue'
import EditorialCover from './EditorialCover.vue'

const props = withDefaults(defineProps<{ book: Book; eager?: boolean; sizes?: string }>(), {
  eager: false,
  sizes: '(max-width: 640px) 44vw, 280px'
})
const edition = computed(() => editionForBook(props.book.title))
</script>

<template>
  <EditorialCover v-if="edition" :edition="edition" :eager="eager" :sizes="sizes" />
  <BookCover v-else :book="book" />
</template>
