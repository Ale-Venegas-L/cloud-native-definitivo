<script setup lang="ts">
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
import BaseCard from '../../UI/BaseCard.vue'

const books = ref<any[]>([])
const authors = ref<any[]>([])
const stats = ref([
  { label: 'Total libros', value: 0, target: 0, color: 'text-ink' },
  { label: 'Total autores', value: 0, target: 0, color: 'text-accent' },
  { label: 'Géneros', value: 0, target: 0, color: 'text-ink-2' }
])

const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

onMounted(async () => {
  try {
    const [booksRes, authorsRes] = await Promise.all([
      fetch(`${apiBase}/books`),
      fetch(`${apiBase}/authors`)
    ])
    books.value = await booksRes.json()
    authors.value = await authorsRes.json()

    const genres = new Set(books.value.map(b => b.genre))

    stats.value[0].target = books.value.length
    stats.value[1].target = authors.value.length
    stats.value[2].target = genres.size

    stats.value.forEach((stat) => {
      const obj = { val: 0 }
      gsap.to(obj, {
        val: stat.target,
        duration: 1.2,
        ease: 'power3.out',
        onUpdate: () => { stat.value = Math.round(obj.val) }
      })
    })
  } catch (e) {
    console.error('Error:', e)
  }
})
</script>

<template>
  <div>
    <h1 class="text-2xl md:text-3xl mb-2">Dashboard</h1>
    <p class="text-ink-3 mb-8">Vista general del sistema.</p>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
      <BaseCard v-for="stat in stats" :key="stat.label" variant="elevated">
        <p :class="['text-3xl font-[var(--font-mono)] tabular-nums', stat.color]">
          {{ stat.value }}
        </p>
        <p class="text-sm text-ink-3 mt-1">{{ stat.label }}</p>
      </BaseCard>
    </div>

    <!-- Recent books -->
    <BaseCard variant="outlined">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg">Libros recientes</h2>
        <router-link to="/admin/stock" class="text-sm text-accent hover:underline">
          Ver todos
        </router-link>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-rule">
              <th class="text-left py-2 text-ink-3 font-medium">Título</th>
              <th class="text-left py-2 text-ink-3 font-medium">Año</th>
              <th class="text-left py-2 text-ink-3 font-medium">Género</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books.slice(0, 5)" :key="book.id" class="border-b border-rule/50">
              <td class="py-2.5 text-ink">{{ book.title }}</td>
              <td class="py-2.5 font-[var(--font-mono)] text-ink-2">{{ book.publication_year }}</td>
              <td class="py-2.5 text-ink-2">{{ book.genre }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>
  </div>
</template>
