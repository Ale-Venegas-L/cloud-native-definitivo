<script setup lang="ts">
import { computed, ref } from 'vue'
import EditorialCover from '../../UI/EditorialCover.vue'
import { editorialEditions } from '../../../data/editions'

type Filter = 'Todas' | 'Facsímil histórico' | 'Edición contemporánea'
const filter = ref<Filter>('Todas')
const visibleEditions = computed(() => filter.value === 'Todas' ? editorialEditions : editorialEditions.filter(edition => edition.kind === filter.value))
</script>

<template>
  <main class="section-space"><div class="page-shell">
    <div class="max-w-3xl"><p class="mb-2 text-xs font-semibold uppercase tracking-[.16em] text-accent">Archivo visual</p><h1 class="text-4xl sm:text-5xl">Ediciones que atraviesan el tiempo</h1><p class="mt-4 text-ink-2">Un recorrido por la materialidad del libro: portadas históricas, facsímiles y lecturas gráficas contemporáneas.</p></div>
    <div class="my-9 flex flex-wrap gap-2" aria-label="Filtrar ediciones"><button v-for="option in ['Todas', 'Facsímil histórico', 'Edición contemporánea'] as Filter[]" :key="option" type="button" :class="['min-h-11 rounded-full border px-4 text-sm font-medium transition-colors', filter === option ? 'border-ink bg-ink text-paper' : 'border-rule text-ink-2 hover:bg-paper-2']" @click="filter = option">{{ option }}</button></div>
    <div class="grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 sm:gap-7 lg:grid-cols-4">
      <article v-for="edition in visibleEditions" :id="edition.id" :key="edition.id" class="scroll-mt-24"><EditorialCover :edition="edition" sizes="(max-width: 640px) 44vw, (max-width: 1024px) 30vw, 260px"/><p class="mt-4 font-[var(--font-mono)] text-[.65rem] uppercase tracking-wider text-accent">{{ edition.kind }} · {{ edition.year }}</p><h2 class="mt-1 text-xl leading-tight sm:text-2xl">{{ edition.title }}</h2><p class="mt-1 text-sm text-ink-3">{{ edition.author }}</p><p class="mt-3 hidden text-sm text-ink-2 sm:block">{{ edition.description }}</p></article>
    </div>
  </div></main>
</template>
