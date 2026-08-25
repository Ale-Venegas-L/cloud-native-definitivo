<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import BookArtwork from '../../UI/BookArtwork.vue'
import ContentState from '../../UI/ContentState.vue'
import ModalBook from '../../composables/modal-book.vue'
import { apiRequest } from '../../../services/api'
import type { Author, Book } from '../../../types/domain'

const books = ref<Book[]>([]), authors = ref<Author[]>([])
const search = ref(''), filterAuthor = ref(''), filterCountry = ref(''), filterGenre = ref('')
const sortBy = ref('title-asc'), filtersOpen = ref(false), loading = ref(true), error = ref('')
const selectedBook = ref<Book | null>(null)
const route = useRoute()
const countries = computed(() => [...new Set(books.value.map(b => b.country))].sort())
const genres = computed(() => [...new Set(books.value.map(b => b.genre))].sort())
const activeFilters = computed(() => [
  search.value && { key: 'search', label: `“${search.value}”` },
  filterAuthor.value && { key: 'author', label: authors.value.find(a => a.id === filterAuthor.value)?.name || 'Autor' },
  filterCountry.value && { key: 'country', label: filterCountry.value },
  filterGenre.value && { key: 'genre', label: filterGenre.value }
].filter(Boolean) as { key: string; label: string }[])
const filteredBooks = computed(() => {
  const result = books.value.filter(book => {
    const query = search.value.trim().toLocaleLowerCase('es')
    const author = authors.value.find(a => a.id === book.author_id)?.name || ''
    return (!query || `${book.title} ${author}`.toLocaleLowerCase('es').includes(query)) && (!filterAuthor.value || book.author_id === filterAuthor.value) && (!filterCountry.value || book.country === filterCountry.value) && (!filterGenre.value || book.genre === filterGenre.value)
  })
  return result.sort((a, b) => sortBy.value === 'year-desc' ? b.publication_year - a.publication_year : sortBy.value === 'year-asc' ? a.publication_year - b.publication_year : sortBy.value === 'title-desc' ? b.title.localeCompare(a.title, 'es') : a.title.localeCompare(b.title, 'es'))
})
function authorName(id: string) { return authors.value.find(a => a.id === id)?.name || 'Desconocido' }
function clearFilter(key?: string) {
  if (!key || key === 'search') search.value = ''
  if (!key || key === 'author') filterAuthor.value = ''
  if (!key || key === 'country') filterCountry.value = ''
  if (!key || key === 'genre') filterGenre.value = ''
}
async function loadData() {
  loading.value = true; error.value = ''
  try {
    [books.value, authors.value] = await Promise.all([apiRequest<Book[]>('/books/'), apiRequest<Author[]>('/authors/')])
    const requestedAuthor = typeof route.query.author === 'string' ? route.query.author : ''
    if (authors.value.some(author => author.id === requestedAuthor)) filterAuthor.value = requestedAuthor
  }
  catch (e) { error.value = e instanceof Error ? e.message : 'No fue posible cargar el catálogo' }
  finally { loading.value = false }
}
onMounted(loadData)
</script>

<template>
  <main class="section-space"><div class="page-shell">
    <div class="mb-10 max-w-2xl"><p class="mb-2 text-xs font-semibold uppercase tracking-[.16em] text-accent">Colección completa</p><h1 class="text-4xl sm:text-5xl">Catálogo</h1><p class="mt-3 text-ink-2">Busca por obra o autor y recorre la colección por país, género o época.</p></div>

    <div class="mb-6 rounded-xl border border-rule bg-paper-2/45 p-3 sm:p-4">
      <div class="flex gap-2">
        <label class="relative flex-1"><span class="sr-only">Buscar libros</span><svg class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><input v-model="search" type="search" placeholder="Buscar título o autor…" class="min-h-12 w-full rounded-md border border-rule bg-paper py-2 pl-11 pr-4 text-sm text-ink placeholder:text-ink-3 focus:border-accent focus:outline-none" /></label>
        <button type="button" class="inline-flex min-h-12 items-center gap-2 rounded-md border border-rule bg-paper px-4 text-sm font-medium text-ink md:hidden" :aria-expanded="filtersOpen" @click="filtersOpen = !filtersOpen">Filtros <span v-if="activeFilters.length" class="rounded-full bg-accent px-1.5 py-0.5 text-xs text-paper">{{ activeFilters.length }}</span></button>
      </div>
      <div :class="['mt-3 grid gap-3 md:grid md:grid-cols-4', filtersOpen ? 'grid' : 'hidden']">
        <select v-model="filterAuthor" class="min-h-11 rounded-md border border-rule bg-paper px-3 text-sm text-ink"><option value="">Todos los autores</option><option v-for="author in authors" :key="author.id" :value="author.id">{{ author.name }}</option></select>
        <select v-model="filterCountry" class="min-h-11 rounded-md border border-rule bg-paper px-3 text-sm text-ink"><option value="">Todos los países</option><option v-for="country in countries" :key="country">{{ country }}</option></select>
        <select v-model="filterGenre" class="min-h-11 rounded-md border border-rule bg-paper px-3 text-sm text-ink"><option value="">Todos los géneros</option><option v-for="genre in genres" :key="genre">{{ genre }}</option></select>
        <select v-model="sortBy" class="min-h-11 rounded-md border border-rule bg-paper px-3 text-sm text-ink" aria-label="Ordenar resultados"><option value="title-asc">Título: A–Z</option><option value="title-desc">Título: Z–A</option><option value="year-desc">Más recientes</option><option value="year-asc">Más antiguos</option></select>
      </div>
    </div>

    <div class="mb-7 flex min-h-8 flex-wrap items-center gap-2"><p class="mr-auto text-sm text-ink-3"><strong class="font-medium text-ink">{{ filteredBooks.length }}</strong> resultado{{ filteredBooks.length === 1 ? '' : 's' }}</p><button v-for="filter in activeFilters" :key="filter.key" type="button" class="inline-flex min-h-8 items-center gap-1 rounded-full bg-accent/10 px-3 text-xs font-medium text-accent" :aria-label="`Quitar filtro ${filter.label}`" @click="clearFilter(filter.key)">{{ filter.label }} <span aria-hidden="true">×</span></button><button v-if="activeFilters.length > 1" type="button" class="min-h-8 px-2 text-xs text-ink-3 underline hover:text-ink" @click="clearFilter()">Limpiar todo</button></div>

    <ContentState v-if="error" title="El catálogo no está disponible" :description="error" tone="error" retryable @retry="loadData" />
    <div v-else-if="loading" class="grid grid-cols-2 gap-x-4 gap-y-9 sm:grid-cols-3 lg:grid-cols-4"><div v-for="n in 8" :key="n"><div class="skeleton aspect-[3/4.35] rounded-lg"/><div class="skeleton mt-4 h-5 w-4/5 rounded"/><div class="skeleton mt-2 h-3 w-1/2 rounded"/></div></div>
    <ContentState v-else-if="filteredBooks.length === 0" title="No encontramos coincidencias" description="Prueba quitando uno de los filtros o utiliza otra búsqueda." />
    <div v-else class="grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 sm:gap-x-6 lg:grid-cols-4">
      <article v-for="book in filteredBooks" :key="book.id" class="group min-w-0"><button type="button" class="block w-full text-left" @click="selectedBook = book"><BookArtwork :book="book" sizes="(max-width: 640px) 44vw, (max-width: 1024px) 30vw, 260px"/><div class="mt-4 flex items-start justify-between gap-2"><div class="min-w-0"><p class="mb-1 font-[var(--font-mono)] text-[.65rem] uppercase tracking-wider text-accent">{{ book.genre }} · {{ book.publication_year }}</p><h2 class="line-clamp-2 text-lg leading-tight transition-colors group-hover:text-accent sm:text-xl">{{ book.title }}</h2><p class="mt-1 truncate text-sm text-ink-3">{{ authorName(book.author_id) }}</p></div><span class="mt-5 hidden text-ink-3 transition-transform group-hover:translate-x-1 sm:block" aria-hidden="true">→</span></div><span class="mt-3 inline-flex min-h-9 items-center text-xs font-medium text-accent sm:hidden">Ver detalles →</span></button></article>
    </div>
    <ModalBook :open="Boolean(selectedBook)" :book="selectedBook" :authors="authors" @close="selectedBook = null" />
  </div></main>
</template>
