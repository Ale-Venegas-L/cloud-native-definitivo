<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useScrollReveal } from '../../../composables/useScrollReveal'

useScrollReveal('.book-reveal')

const books = ref<any[]>([])
const authors = ref<any[]>([])
const search = ref('')
const filterAuthor = ref('')
const filterCountry = ref('')
const filterGenre = ref('')

const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const countries = computed(() => [...new Set(books.value.map(b => b.country))])
const genres = computed(() => [...new Set(books.value.map(b => b.genre))])

const filteredBooks = computed(() => {
  return books.value.filter(book => {
    const matchSearch = !search.value || book.title.toLowerCase().includes(search.value.toLowerCase())
    const matchAuthor = !filterAuthor.value || book.author_id === filterAuthor.value
    const matchCountry = !filterCountry.value || book.country === filterCountry.value
    const matchGenre = !filterGenre.value || book.genre === filterGenre.value
    return matchSearch && matchAuthor && matchCountry && matchGenre
  })
})

function getAuthorName(authorId: string): string {
  const author = authors.value.find(a => a.id === authorId)
  return author?.name || 'Desconocido'
}

onMounted(async () => {
  try {
    const [booksRes, authorsRes] = await Promise.all([
      fetch(`${apiBase}/books`),
      fetch(`${apiBase}/authors`)
    ])
    books.value = await booksRes.json()
    authors.value = await authorsRes.json()
  } catch (e) {
    console.error('Error cargando datos:', e)
  }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-5 py-xl">
    <div class="mb-10">
      <h1 class="text-3xl md:text-4xl mb-2">Catálogo</h1>
      <p class="text-ink-2">Explora nuestra colección de obras clásicas.</p>
    </div>

    <!-- Filters -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-3 mb-8">
      <input
        v-model="search"
        type="text"
        placeholder="Buscar por título..."
        class="px-4 py-2.5 bg-paper-2 border border-rule rounded-[var(--radius-md)]
               text-ink placeholder:text-ink-3 text-sm
               focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/20
               transition-all duration-[var(--dur-short)]"
      >
      <select
        v-model="filterAuthor"
        class="px-4 py-2.5 bg-paper-2 border border-rule rounded-[var(--radius-md)]
               text-ink text-sm appearance-none
               focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/20
               transition-all duration-[var(--dur-short)]"
      >
        <option value="">Todos los autores</option>
        <option v-for="author in authors" :key="author.id" :value="author.id">{{ author.name }}</option>
      </select>
      <select
        v-model="filterCountry"
        class="px-4 py-2.5 bg-paper-2 border border-rule rounded-[var(--radius-md)]
               text-ink text-sm appearance-none
               focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/20
               transition-all duration-[var(--dur-short)]"
      >
        <option value="">Todos los países</option>
        <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
      </select>
      <select
        v-model="filterGenre"
        class="px-4 py-2.5 bg-paper-2 border border-rule rounded-[var(--radius-md)]
               text-ink text-sm appearance-none
               focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/20
               transition-all duration-[var(--dur-short)]"
      >
        <option value="">Todos los géneros</option>
        <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
      </select>
    </div>

    <!-- Results count -->
    <p class="text-sm text-ink-3 mb-5">
      {{ filteredBooks.length }} libro{{ filteredBooks.length !== 1 ? 's' : '' }}
    </p>

    <!-- Books grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="book in filteredBooks"
        :key="book.id"
        class="book-reveal group p-5 bg-paper-2 border border-rule rounded-[var(--radius-lg)]
               hover:shadow-[var(--shadow-card)] hover:border-accent/30
               transition-all duration-[var(--dur-short)] ease-[var(--ease-out)]"
      >
        <div class="flex items-start justify-between mb-3">
          <span class="text-xs font-[var(--font-mono)] text-ink-3 tracking-wide uppercase">
            {{ book.genre }}
          </span>
          <span class="text-xs font-[var(--font-mono)] text-accent">
            {{ book.publication_year }}
          </span>
        </div>
        <h3 class="text-lg group-hover:text-accent transition-colors mb-1">
          {{ book.title }}
        </h3>
        <p class="text-sm text-ink-2 mb-3">{{ getAuthorName(book.author_id) }}</p>
        <div class="flex items-center justify-between">
          <span class="text-xs text-ink-3">{{ book.country }}</span>
          <span
            v-if="book.cover_url"
            class="w-8 h-10 bg-paper-3 rounded-sm flex items-center justify-center text-ink-3"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </span>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="filteredBooks.length === 0 && books.length > 0" class="text-center py-16">
      <p class="text-ink-3 text-lg">No se encontraron libros con esos filtros.</p>
    </div>
  </div>
</template>
