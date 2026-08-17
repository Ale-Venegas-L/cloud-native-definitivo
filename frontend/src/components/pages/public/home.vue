<script setup lang="ts">
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
import { useScrollReveal } from '../../../composables/useScrollReveal'

useScrollReveal('.home-reveal')

const stats = ref([
  { label: 'Libros', value: 0, target: 9 },
  { label: 'Autores', value: 0, target: 5 },
  { label: 'Países', value: 0, target: 3 }
])

onMounted(() => {
  stats.value.forEach((stat) => {
    const obj = { val: 0 }
    gsap.to(obj, {
      val: stat.target,
      duration: 1.4,
      delay: 0.6,
      ease: 'power3.out',
      onUpdate: () => {
        stat.value = Math.round(obj.val)
      }
    })
  })
})
</script>

<template>
  <div>
    <!-- Hero -->
    <section class="px-5 py-2xl md:py-3xl">
      <div class="max-w-6xl mx-auto">
        <p class="text-sm font-medium text-accent tracking-wide uppercase mb-4">
          Biblioteca de literatura clásica
        </p>
        <h1 class="text-[var(--text-display)] leading-[1.1] tracking-tight mb-6">
          Obras que definieron<br>la literatura mundial
        </h1>
        <p class="text-lg text-ink-2 max-w-xl leading-relaxed mb-8">
          Explora una colección curada de obras maestras organizadas por autor,
          país y año de publicación.
        </p>
        <router-link
          to="/books"
          class="inline-flex items-center gap-2 px-6 py-3 bg-ink text-paper rounded-[var(--radius-md)]
                 text-sm font-medium hover:bg-ink/90 active:bg-ink/80
                 transition-all duration-[var(--dur-short)] ease-[var(--ease-out)]"
        >
          Explorar catálogo
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </router-link>
      </div>
    </section>

    <!-- Stats -->
    <section class="px-5 py-xl border-t border-rule">
      <div class="max-w-6xl mx-auto grid grid-cols-3 gap-8">
        <div v-for="stat in stats" :key="stat.label" class="text-center">
          <p class="text-3xl md:text-4xl font-[var(--font-mono)] text-ink tabular-nums">
            {{ stat.value }}
          </p>
          <p class="text-sm text-ink-3 mt-1">{{ stat.label }}</p>
        </div>
      </div>
    </section>

    <!-- Featured section -->
    <section class="px-5 py-2xl border-t border-rule home-reveal">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-2xl md:text-3xl mb-2">Autores destacados</h2>
        <p class="text-ink-3 mb-8">Conoce a los autores que moldearon la literatura.</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <router-link
            to="/books"
            class="group block p-5 bg-paper-2 border border-rule rounded-[var(--radius-lg)]
                   hover:shadow-[var(--shadow-card)] hover:border-accent/30
                   transition-all duration-[var(--dur-short)] ease-[var(--ease-out)]"
          >
            <p class="text-xs text-ink-3 font-[var(--font-mono)] tracking-wide uppercase">España · 1547–1616</p>
            <h3 class="text-xl mt-2 group-hover:text-accent transition-colors">Miguel de Cervantes</h3>
            <p class="text-sm text-ink-2 mt-2 line-clamp-2">
              Novelista, poeta y dramaturgo español. Autor de Don Quijote de la Mancha.
            </p>
          </router-link>
          <router-link
            to="/books"
            class="group block p-5 bg-paper-2 border border-rule rounded-[var(--radius-lg)]
                   hover:shadow-[var(--shadow-card)] hover:border-accent/30
                   transition-all duration-[var(--dur-short)] ease-[var(--ease-out)]"
          >
            <p class="text-xs text-ink-3 font-[var(--font-mono)] tracking-wide uppercase">Colombia · 1927–2014</p>
            <h3 class="text-xl mt-2 group-hover:text-accent transition-colors">Gabriel García Márquez</h3>
            <p class="text-sm text-ink-2 mt-2 line-clamp-2">
              Premio Nobel de Literatura 1982. Padre del realismo mágico.
            </p>
          </router-link>
          <router-link
            to="/books"
            class="group block p-5 bg-paper-2 border border-rule rounded-[var(--radius-lg)]
                   hover:shadow-[var(--shadow-card)] hover:border-accent/30
                   transition-all duration-[var(--dur-short)] ease-[var(--ease-out)]"
          >
            <p class="text-xs text-ink-3 font-[var(--font-mono)] tracking-wide uppercase">Inglaterra · 1564–1616</p>
            <h3 class="text-xl mt-2 group-hover:text-accent transition-colors">William Shakespeare</h3>
            <p class="text-sm text-ink-2 mt-2 line-clamp-2">
              Dramaturgo y poeta inglés. Autor de Hamlet y Romeo y Julieta.
            </p>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>
