<script setup lang="ts">
import type { EditorialEdition } from '../../data/editions'

withDefaults(defineProps<{ edition: EditorialEdition; eager?: boolean; sizes?: string }>(), {
  eager: false,
  sizes: '(max-width: 640px) 44vw, 280px'
})
</script>

<template>
  <div class="editorial-cover">
    <img
      :src="edition.medium"
      :srcset="`${edition.small} 320w, ${edition.medium} 640w`"
      :sizes="sizes"
      :alt="edition.alt"
      width="640"
      height="960"
      :loading="eager ? 'eager' : 'lazy'"
      :fetchpriority="eager ? 'high' : 'auto'"
      decoding="async"
    >
  </div>
</template>

<style scoped>
.editorial-cover {
  display: grid;
  aspect-ratio: 2 / 3;
  place-items: center;
  overflow: hidden;
  border: 1px solid var(--color-rule);
  border-radius: var(--radius-md);
  background: var(--color-paper-2);
  box-shadow: var(--shadow-card);
}

.editorial-cover img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
