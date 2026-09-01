<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import gsap from 'gsap'
import BaseCard from '../../UI/BaseCard.vue'
import ContentState from '../../UI/ContentState.vue'
import { apiRequest } from '../../../services/api'
import type { Author, Book } from '../../../types/domain'

const books = ref<Book[]>([]), authors = ref<Author[]>([])
const loading = ref(true), error = ref('')
const stats = ref([{ label: 'Libros', value: 0, target: 0 }, { label: 'Autores', value: 0, target: 0 }, { label: 'Géneros', value: 0, target: 0 }])
const genreDistribution = computed(() => {
  const counts = books.value.reduce<Record<string, number>>((all, book) => ({ ...all, [book.genre]: (all[book.genre] || 0) + 1 }), {})
  return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([name, count]) => ({ name, count, percent: books.value.length ? Math.round(count / books.value.length * 100) : 0 }))
})
function authorName(id: string) { return authors.value.find(author => author.id === id)?.name || '—' }
async function loadDashboard() {
  loading.value = true; error.value = ''
  try {
    [books.value, authors.value] = await Promise.all([apiRequest<Book[]>('/books/'), apiRequest<Author[]>('/authors/')])
    const targets = [books.value.length, authors.value.length, new Set(books.value.map(book => book.genre)).size]
    stats.value.forEach((stat, index) => { stat.target = targets[index] || 0; gsap.to(stat, { value: stat.target, duration: .9, ease: 'power3.out', snap: { value: 1 } }) })
  } catch (e) { error.value = e instanceof Error ? e.message : 'No fue posible cargar el dashboard' }
  finally { loading.value = false }
}
onMounted(loadDashboard)
</script>

<template>
  <div>
    <div class="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p class="mb-2 text-xs font-semibold uppercase tracking-[.15em] text-accent">Vista general</p><h1 class="text-3xl sm:text-4xl">Dashboard</h1><p class="mt-2 text-sm text-ink-3">Estado actual de la colección.</p></div><router-link to="/admin/stock" class="inline-flex min-h-11 items-center justify-center rounded-md bg-ink px-5 text-sm font-medium text-paper">Gestionar biblioteca</router-link></div>
    <ContentState v-if="error" title="No pudimos cargar el panel" :description="error" tone="error" retryable @retry="loadDashboard" />
    <template v-else>
      <div class="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <BaseCard v-for="(stat, index) in stats" :key="stat.label" variant="outlined" class="relative overflow-hidden"><div class="flex items-start justify-between"><div><p class="font-[var(--font-mono)] text-3xl tabular-nums">{{ loading ? '—' : stat.value }}</p><p class="mt-1 text-sm text-ink-3">{{ stat.label }}</p></div><span class="flex h-10 w-10 items-center justify-center rounded-full bg-accent/10 text-sm font-medium text-accent">0{{ index + 1 }}</span></div></BaseCard>
      </div>
      <div class="grid gap-6 xl:grid-cols-[1.4fr_.8fr]">
        <BaseCard variant="outlined"><div class="mb-5 flex items-center justify-between"><div><h2 class="text-xl">Últimas incorporaciones</h2><p class="mt-1 text-xs text-ink-3">Los registros más recientes del catálogo</p></div><router-link to="/admin/stock" class="text-sm">Ver todos →</router-link></div>
          <div v-if="loading" class="space-y-3"><div v-for="n in 4" :key="n" class="skeleton h-14 rounded-md" /></div>
          <div v-else-if="books.length" class="divide-y divide-rule"><div v-for="book in books.slice(0, 5)" :key="book.id" class="flex items-center gap-4 py-3"><div class="flex h-11 w-9 shrink-0 items-center justify-center rounded bg-ink font-[var(--font-display)] text-paper">{{ book.title.charAt(0) }}</div><div class="min-w-0 flex-1"><p class="truncate text-sm font-medium text-ink">{{ book.title }}</p><p class="truncate text-xs text-ink-3">{{ authorName(book.author_id) }}</p></div><div class="hidden text-right sm:block"><p class="font-[var(--font-mono)] text-xs text-ink-2">{{ book.publication_year }}</p><p class="text-xs text-ink-3">{{ book.genre }}</p></div></div></div>
          <p v-else class="py-8 text-center text-sm text-ink-3">Todavía no hay libros registrados.</p>
        </BaseCard>
        <div class="grid gap-6">
          <BaseCard variant="outlined"><h2 class="mb-5 text-xl">Géneros</h2><div v-if="genreDistribution.length" class="space-y-4"><div v-for="genre in genreDistribution" :key="genre.name"><div class="mb-1.5 flex justify-between text-xs"><span class="text-ink-2">{{ genre.name }}</span><span class="font-[var(--font-mono)] text-ink-3">{{ genre.count }}</span></div><div class="h-1.5 overflow-hidden rounded-full bg-paper-3"><div class="h-full rounded-full bg-accent" :style="{ width: `${genre.percent}%` }" /></div></div></div><p v-else class="text-sm text-ink-3">Sin datos disponibles.</p></BaseCard>
          <BaseCard variant="outlined"><h2 class="text-xl">Acciones rápidas</h2><div class="mt-4 grid gap-2"><router-link to="/admin/stock?create=book" class="flex min-h-11 items-center justify-between rounded-md bg-paper-2 px-4 text-sm font-medium text-ink hover:bg-paper-3">Añadir libro <span>＋</span></router-link><router-link to="/admin/stock?create=author" class="flex min-h-11 items-center justify-between rounded-md bg-paper-2 px-4 text-sm font-medium text-ink hover:bg-paper-3">Añadir autor <span>＋</span></router-link><router-link to="/" class="flex min-h-11 items-center justify-between rounded-md px-4 text-sm font-medium text-ink-2 hover:bg-paper-2">Ver sitio público <span>↗</span></router-link></div></BaseCard>
        </div>
      </div>
    </template>
  </div>
</template>
