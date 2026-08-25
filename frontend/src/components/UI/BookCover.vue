<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Book } from '../../types/domain'
const props = defineProps<{ book: Book; compact?: boolean }>()
const imageFailed = ref(false)
watch(() => props.book.cover_url, () => { imageFailed.value = false })
</script>

<template>
  <div :class="['relative isolate overflow-hidden rounded-[var(--radius-md)] bg-[#14151A] text-[#E3D5C1] shadow-[var(--shadow-card)]', compact ? 'aspect-[3/4]' : 'aspect-[3/4.35]']">
    <img v-if="book.cover_url && !imageFailed" :src="book.cover_url" :alt="`Portada de ${book.title}`" class="h-full w-full object-cover" loading="lazy" @error="imageFailed = true">
    <div v-else class="flex h-full flex-col justify-between overflow-hidden p-[12%]" :style="{ background: `linear-gradient(145deg, color-mix(in oklch, var(--color-5) ${35 + book.publication_year % 25}%, var(--color-3)), var(--color-3))` }">
      <div class="h-px w-8 bg-[#E3D5C1]/70" />
      <div>
        <p class="mb-2 font-[var(--font-mono)] text-[clamp(.52rem,1.5vw,.68rem)] uppercase tracking-[.16em] text-[#E3D5C1]/65">Classic Library</p>
        <p class="font-[var(--font-display)] text-[clamp(1rem,3vw,1.7rem)] leading-[1.02] text-[#E3D5C1]">{{ book.title }}</p>
      </div>
      <p class="font-[var(--font-mono)] text-[.6rem] text-[#E3D5C1]/60">{{ book.publication_year }}</p>
      <span class="absolute -bottom-8 -right-8 h-28 w-28 rounded-full border border-[#E3D5C1]/15" />
      <span class="absolute -bottom-3 -right-3 h-16 w-16 rounded-full border border-[#E3D5C1]/15" />
    </div>
  </div>
</template>
