<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import gsap from 'gsap'
import EditorialCover from '../../UI/EditorialCover.vue'
import ContentState from '../../UI/ContentState.vue'
import { apiRequest } from '../../../services/api'
import { editorialEditions, editionsForAuthor } from '../../../data/editions'
import type { Author, Book } from '../../../types/domain'
import heroImage from '../../../assets/img/hero/hero-home.webp'
import editorialBackground from '../../../assets/img/hero/background-archivo-editorial.webp'
import cervantesPortrait from '../../../assets/img/authors/miguel-de-cervantes.webp'
import shakespearePortrait from '../../../assets/img/authors/william-shakespeare.webp'
import garciaMarquezPortrait from '../../../assets/img/authors/gabriel-garcia-marquez.webp'

interface AuthorProfile {
  movement: string
  specialty: string
  note: string
  portrait: string
}

const authorProfiles: Record<string, AuthorProfile> = {
  'miguel de cervantes': {
    movement: 'Siglo de Oro',
    specialty: 'Novela moderna',
    note: 'La ficción como espejo de la libertad y la condición humana.',
    portrait: cervantesPortrait
  },
  'william shakespeare': {
    movement: 'Teatro isabelino',
    specialty: 'Drama y poesía',
    note: 'El escenario convertido en un mapa de las pasiones humanas.',
    portrait: shakespearePortrait
  },
  'gabriel garcia marquez': {
    movement: 'Boom latinoamericano',
    specialty: 'Realismo mágico',
    note: 'Lo extraordinario narrado con la naturalidad de lo cotidiano.',
    portrait: garciaMarquezPortrait
  }
}

function normalizeName(value: string) {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('es').trim()
}

const books = ref<Book[]>([])
const authors = ref<Author[]>([])
const loading = ref(true)
const error = ref('')
const counts = ref({ books: 0, authors: 0, countries: 0 })
const statTargets = ref({ books: 0, authors: 0, countries: 0 })
const libraryStats = computed(() => [
  { key: 'books', code: 'COL—001', label: 'Libros', value: counts.value.books, description: 'obras preservadas', detail: 'Colección' },
  { key: 'authors', code: 'AUT—005', label: 'Autores', value: counts.value.authors, description: 'voces imprescindibles', detail: 'Índice de autor' },
  { key: 'countries', code: 'ORI—004', label: 'Países', value: counts.value.countries, description: 'tradiciones literarias', detail: 'Procedencia' }
])
const featuredAuthors = computed(() => {
  const preferred = ['miguel de cervantes', 'william shakespeare', 'gabriel garcia marquez']
    .map(name => authors.value.find(author => normalizeName(author.name) === name))
    .filter((author): author is Author => Boolean(author))
  return preferred.length === 3 ? preferred : authors.value.slice(0, 3)
})
const editionRail = ref<HTMLElement | null>(null)
const authorSection = ref<HTMLElement | null>(null)
const statsSection = ref<HTMLElement | null>(null)
const editionCopies = [0, 1, 2]
let animationFrame = 0
let resumeTimer = 0
let previousFrame = 0
let loopWidth = 0
let loopStart = 0
let autoScrollPosition = 0
let railPaused = false
let railVisible = true
let reducedMotion: MediaQueryList | undefined
let resizeObserver: ResizeObserver | undefined
let intersectionObserver: IntersectionObserver | undefined
let authorObserver: IntersectionObserver | undefined
let statsObserver: IntersectionObserver | undefined
let statsAnimated = false

function setupStatsReveal() {
  statsObserver?.disconnect()
  const section = statsSection.value
  if (!section || statsAnimated) return
  statsObserver = new IntersectionObserver(([entry]) => {
    if (!entry?.isIntersecting) return
    statsAnimated = true
    const cards = section.querySelectorAll('.stat-volume')
    const progress = section.querySelector('.stats-progress')
    if (reducedMotion?.matches) {
      Object.assign(counts.value, statTargets.value)
    } else {
      const progressAxis = window.matchMedia('(max-width: 767px)').matches ? 'scaleY' : 'scaleX'
      gsap.fromTo(progress, { [progressAxis]: 0 }, { [progressAxis]: 1, duration: 1.25, ease: 'power3.inOut' })
      gsap.fromTo(cards, { autoAlpha: 0, y: 22 }, { autoAlpha: 1, y: 0, duration: 0.72, stagger: 0.12, ease: 'power3.out', clearProps: 'opacity,transform,visibility' })
      gsap.to(counts.value, { ...statTargets.value, duration: 1.15, delay: 0.16, ease: 'power3.out', snap: { books: 1, authors: 1, countries: 1 } })
    }
    statsObserver?.disconnect()
  }, { threshold: 0.22 })
  statsObserver.observe(section)
}

function authorProfile(author: Author): AuthorProfile {
  return authorProfiles[normalizeName(author.name)] || {
    movement: 'Literatura universal',
    specialty: 'Autor destacado',
    note: 'Una voz imprescindible dentro de la historia de la literatura.',
    portrait: author.image_url || ''
  }
}

function authorBookCount(author: Author) {
  return books.value.filter(book => book.author_id === author.id).length
}

function authorFirstBook(author: Author) {
  return books.value.find(book => book.author_id === author.id)
}

function authorEdition(author: Author) {
  return editionsForAuthor(author.name)[0]
}

function setupAuthorReveal() {
  authorObserver?.disconnect()
  const section = authorSection.value
  if (!section) return
  const cards = Array.from(section.querySelectorAll<HTMLElement>('.author-card'))
  if (reducedMotion?.matches) return
  authorObserver = new IntersectionObserver(([entry]) => {
    if (!entry?.isIntersecting) return
    gsap.fromTo(cards, { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.72, stagger: 0.11, ease: 'power3.out', clearProps: 'opacity,transform,visibility' })
    authorObserver?.disconnect()
  }, { threshold: 0.16 })
  authorObserver.observe(section)
}

function measureEditionRail() {
  const rail = editionRail.value
  if (!rail) return
  const starts = rail.querySelectorAll<HTMLElement>('[data-edition-start]')
  if (starts.length !== editionCopies.length) return
  loopWidth = starts[2]!.offsetLeft - starts[1]!.offsetLeft
  loopStart = starts[1]!.offsetLeft - Number.parseFloat(getComputedStyle(rail).paddingLeft)
  if (loopWidth && (rail.scrollLeft < loopStart - loopWidth || rail.scrollLeft > loopStart + loopWidth)) rail.scrollLeft = loopStart
  autoScrollPosition = rail.scrollLeft
}

function normalizeEditionRail() {
  const rail = editionRail.value
  if (!rail || !loopWidth) return
  if (rail.scrollLeft >= loopStart + loopWidth) {
    rail.scrollLeft -= loopWidth
    autoScrollPosition -= loopWidth
  } else if (rail.scrollLeft <= loopStart - loopWidth) {
    rail.scrollLeft += loopWidth
    autoScrollPosition += loopWidth
  } else if (railPaused) {
    autoScrollPosition = rail.scrollLeft
  }
}

function animateEditionRail(timestamp: number) {
  const rail = editionRail.value
  if (rail && previousFrame && !railPaused && railVisible) {
    const elapsed = Math.min(timestamp - previousFrame, 50)
    const speed = reducedMotion?.matches ? 0.014 : 0.032
    autoScrollPosition += elapsed * speed
    rail.scrollLeft = autoScrollPosition
    normalizeEditionRail()
  }
  previousFrame = timestamp
  animationFrame = requestAnimationFrame(animateEditionRail)
}

function beginRailInteraction() {
  window.clearTimeout(resumeTimer)
  if (editionRail.value) autoScrollPosition = editionRail.value.scrollLeft
  railPaused = true
}

function resumeRailAfterDelay() {
  window.clearTimeout(resumeTimer)
  resumeTimer = window.setTimeout(() => {
    if (editionRail.value) autoScrollPosition = editionRail.value.scrollLeft
    railPaused = false
  }, 2000)
}

function pauseRailTemporarily() {
  beginRailInteraction()
  resumeRailAfterDelay()
}

async function loadHome() {
  loading.value = true; error.value = ''
  try {
    const [bookData, authorData] = await Promise.all([apiRequest<Book[]>('/books/'), apiRequest<Author[]>('/authors/')])
    books.value = bookData; authors.value = authorData
    await nextTick()
    setupAuthorReveal()
    statTargets.value = { books: bookData.length, authors: authorData.length, countries: new Set(bookData.map(book => book.country)).size }
    setupStatsReveal()
  } catch (e) { error.value = e instanceof Error ? e.message : 'No fue posible cargar la biblioteca' }
  finally { loading.value = false }
}
onMounted(async () => {
  loadHome()
  await nextTick()
  measureEditionRail()
  reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
  resizeObserver = new ResizeObserver(measureEditionRail)
  if (editionRail.value) resizeObserver.observe(editionRail.value)
  intersectionObserver = new IntersectionObserver(([entry]) => { railVisible = Boolean(entry?.isIntersecting) }, { threshold: 0.05 })
  if (editionRail.value) intersectionObserver.observe(editionRail.value)
  animationFrame = requestAnimationFrame(animateEditionRail)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(animationFrame)
  window.clearTimeout(resumeTimer)
  resizeObserver?.disconnect()
  intersectionObserver?.disconnect()
  authorObserver?.disconnect()
  statsObserver?.disconnect()
})
</script>

<template>
  <div>
    <section class="relative isolate min-h-dvh overflow-hidden border-b border-rule bg-[#14151A]">
      <img :src="heroImage" alt="Sala de una biblioteca clásica iluminada por luz natural" class="absolute inset-0 -z-20 h-full w-full object-cover object-[58%_center] sm:object-center" width="1376" height="768" fetchpriority="high" decoding="async">
      <div class="page-shell flex min-h-dvh items-center py-24 sm:py-28">
        <div class="relative z-10 max-w-3xl">
          <p class="mb-4 text-xs font-semibold uppercase tracking-[.18em] text-accent">Biblioteca de literatura clásica</p>
          <h1 class="hero-title text-[clamp(3rem,7vw,5.75rem)] leading-[.95] tracking-[-.035em]">Historias que aún<br class="hidden sm:block"> hablan de nosotros</h1>
          <p class="mt-7 max-w-xl text-base leading-relaxed text-[#E3D5C1]/80 sm:text-lg">Una colección curada de obras maestras para descubrir autores, épocas y países que transformaron la literatura.</p>
          <div class="mt-8 flex flex-col gap-3 sm:flex-row">
            <router-link to="/books" class="inline-flex min-h-12 items-center justify-center gap-2 rounded-md bg-[#E3D5C1] px-6 text-sm font-medium text-[#14151A] transition-transform hover:-translate-y-0.5 hover:bg-[#AFB2B4] hover:text-[#14151A]">Explorar catálogo <span aria-hidden="true">→</span></router-link>
            <a href="#seleccion" class="inline-flex min-h-12 items-center justify-center rounded-md border border-[#E3D5C1]/35 bg-[#14151A]/20 px-6 text-sm font-medium text-[#E3D5C1] backdrop-blur hover:bg-[#E3D5C1]/12 hover:text-[#E3D5C1]">Ver selección</a>
          </div>
        </div>
      </div>
    </section>

    <section ref="statsSection" class="stats-library" aria-labelledby="collection-index-title">
      <div class="page-shell py-12 sm:py-16">
        <div class="stats-heading">
          <div>
            <p class="stats-eyebrow">Colección permanente · Archivo vivo</p>
            <h2 id="collection-index-title" class="stats-title mt-2 text-3xl sm:text-4xl">Índice de la biblioteca</h2>
          </div>
          <p class="stats-summary hidden max-w-xs text-right text-sm leading-relaxed md:block">Una lectura cuantitativa de las obras, las voces y los territorios reunidos en el archivo.</p>
        </div>

        <div class="stats-shelf">
          <div class="stats-line" aria-hidden="true"><span class="stats-progress" /></div>
          <article v-for="(stat, index) in libraryStats" :key="stat.key" class="stat-volume">
            <span class="stat-node" aria-hidden="true" />
            <div class="stat-volume-top">
              <span class="stat-code">{{ stat.code }}</span>
              <svg v-if="index === 0" class="stat-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H11v16H6.5A2.5 2.5 0 0 0 4 21.5v-16ZM20 5.5A2.5 2.5 0 0 0 17.5 3H13v16h4.5a2.5 2.5 0 0 1 2.5 2.5v-16Z"/></svg>
              <svg v-else-if="index === 1" class="stat-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 13.5a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM4.5 21c.7-3.4 3.4-5.5 7.5-5.5s6.8 2.1 7.5 5.5"/></svg>
              <svg v-else class="stat-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.3 2.5 3.5 5.5 3.5 9S14.3 18.5 12 21c-2.3-2.5-3.5-5.5-3.5-9S9.7 5.5 12 3Z"/></svg>
            </div>
            <div class="stat-number-row">
              <strong class="stat-number">{{ stat.value }}</strong>
              <span class="stat-seal">Registro<br>activo</span>
            </div>
            <div class="stat-copy">
              <p class="stat-label">{{ stat.label }}</p>
              <p class="stat-description">{{ stat.description }}</p>
            </div>
            <p class="stat-detail">{{ stat.detail }}</p>
          </article>
        </div>
      </div>
    </section>

    <section
      id="seleccion"
      class="editorial-section section-space overflow-hidden"
      :style="{ '--editorial-background': `url(${editorialBackground})` }"
    ><div class="page-shell">
      <div class="mb-9 flex items-end justify-between gap-5"><div><p class="mb-2 text-xs font-semibold uppercase tracking-[.16em] text-accent">Archivo editorial</p><h2 class="text-3xl sm:text-4xl">Ediciones que atraviesan el tiempo</h2><p class="mt-3 max-w-xl text-sm text-ink-2">De los primeros impresos a interpretaciones gráficas contemporáneas.</p></div><router-link to="/editions" class="hidden shrink-0 text-sm font-medium sm:block">Explorar archivo →</router-link></div>
      <div
        ref="editionRail"
        class="edition-rail"
        aria-label="Selección de ediciones en movimiento continuo"
        @focusin="pauseRailTemporarily"
        @keydown="pauseRailTemporarily"
        @wheel.passive="pauseRailTemporarily"
        @pointerdown="beginRailInteraction"
        @pointerup="resumeRailAfterDelay"
        @pointercancel="resumeRailAfterDelay"
        @pointerleave="resumeRailAfterDelay"
        @scroll.passive="normalizeEditionRail"
      >
        <template v-for="copy in editionCopies" :key="copy">
          <router-link
            v-for="edition in editorialEditions"
            :key="`${copy}-${edition.id}`"
            :to="`/editions#${edition.id}`"
            class="edition-item group text-ink"
            :data-edition-start="edition === editorialEditions[0] ? '' : undefined"
            :aria-hidden="copy === 1 ? undefined : 'true'"
            :tabindex="copy === 1 ? undefined : -1"
          >
            <EditorialCover :edition="edition" sizes="(max-width: 640px) 68vw, 250px" />
            <p class="mt-4 font-[var(--font-mono)] text-[.65rem] uppercase tracking-wider text-accent">{{ edition.kind }} · {{ edition.year }}</p>
            <h3 class="mt-1 text-xl leading-tight transition-colors group-hover:text-accent">{{ edition.title }}</h3>
            <p class="mt-1 text-sm text-ink-3">{{ edition.author }}</p>
          </router-link>
        </template>
      </div>
      <router-link to="/editions" class="mt-8 inline-flex min-h-11 items-center text-sm font-medium sm:hidden">Explorar archivo →</router-link>
    </div></section>

    <section ref="authorSection" class="authors-section section-space border-t border-rule"><div class="page-shell">
      <div class="mb-9 flex items-end justify-between gap-6 sm:mb-11">
        <div class="max-w-2xl">
          <p class="mb-2 text-xs font-semibold uppercase tracking-[.16em] text-accent">Voces imprescindibles</p>
          <h2 class="text-3xl sm:text-4xl">Autores destacados</h2>
          <p class="mt-3 text-sm leading-relaxed text-ink-2">Tres voces, tres épocas y una misma capacidad para transformar nuestra manera de leer el mundo.</p>
        </div>
        <router-link to="/books" class="hidden shrink-0 text-sm font-medium sm:inline-flex">Ver todos los autores →</router-link>
      </div>

      <ContentState v-if="error" title="No pudimos cargar los autores" :description="error" tone="error" retryable @retry="loadHome" />
      <div v-else class="author-grid">
        <router-link
          v-for="(author, index) in featuredAuthors"
          :key="author.id"
          :to="{ path: '/books', query: { author: author.id } }"
          :class="['author-card group', { 'author-card--lead': index === 0 }]"
        >
          <span class="author-tab">Ficha de autor</span>
          <div class="author-portrait" aria-hidden="true">
            <img :src="authorProfile(author).portrait" alt="" width="640" height="800" loading="lazy" decoding="async">
          </div>

          <div v-if="authorEdition(author)" class="author-edition" aria-hidden="true">
            <EditorialCover :edition="authorEdition(author)!" sizes="82px" />
          </div>
          <div v-else-if="authorFirstBook(author)" class="author-edition author-bookplate" aria-hidden="true">
            <span>Biblioteca</span>
            <strong>{{ authorFirstBook(author)!.title }}</strong>
          </div>

          <div class="author-content">
            <div class="flex items-center gap-3">
              <span class="author-code">AUT—{{ String(index + 1).padStart(3, '0') }}</span>
              <span class="h-px w-8 bg-accent/55 transition-[width] duration-300 group-hover:w-14" />
            </div>
            <p class="mt-7 font-[var(--font-mono)] text-[.65rem] uppercase tracking-[.13em] text-ink-3">{{ author.country }} · {{ author.birth_year }}–{{ author.death_year || 'presente' }}</p>
            <h3 class="mt-2 max-w-[12ch] text-[clamp(1.85rem,3.2vw,3rem)] leading-[.96] tracking-[-.025em]">{{ author.name }}</h3>
            <p v-if="author.biography" class="author-biography mt-5 max-w-md text-sm leading-relaxed text-ink-2">{{ author.biography }}</p>
            <p class="author-note mt-5 max-w-sm border-l border-accent/60 pl-4 font-[var(--font-display)] text-lg italic leading-snug text-ink-2">{{ authorProfile(author).note }}</p>

            <div class="author-facts mt-auto flex flex-wrap gap-x-5 gap-y-1 pt-6 font-[var(--font-mono)] text-[.62rem] uppercase tracking-[.1em] text-ink-3">
              <span>{{ authorProfile(author).movement }}</span>
              <span>{{ authorProfile(author).specialty }}</span>
              <span>{{ authorBookCount(author) }} obra{{ authorBookCount(author) === 1 ? '' : 's' }}</span>
            </div>
            <span class="author-cta mt-5 inline-flex items-center gap-2 text-sm font-medium text-accent">Explorar sus obras <span aria-hidden="true">→</span></span>
          </div>
        </router-link>
      </div>
      <router-link to="/books" class="mt-7 inline-flex min-h-11 items-center text-sm font-medium sm:hidden">Ver todos los autores →</router-link>
    </div></section>
  </div>
</template>

<style scoped>
.hero-title {
  color: #E3D5C1;
}

.stats-library {
  position: relative;
  contain: paint;
  overflow: hidden;
  border-bottom: 1px solid rgb(141 128 111 / 0.5);
  background-color: var(--stats-bg);
  background-image:
    radial-gradient(circle at 82% 12%, var(--stats-bg-accent), transparent 28rem),
    repeating-linear-gradient(90deg, transparent 0, transparent 5rem, var(--stats-grid) 5rem, var(--stats-grid) calc(5rem + 1px));
  color: var(--stats-ink);
}

.stats-heading {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--stats-rule);
}

.stats-title { color: var(--stats-ink); }
.stats-summary { color: var(--stats-muted); }

.stats-eyebrow {
  color: var(--color-accent);
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.stats-shelf {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: end;
  gap: clamp(0.75rem, 2vw, 1.25rem);
  padding: 4rem 0 3.8rem;
  border-bottom: 0.72rem solid var(--stats-shelf);
  box-shadow: 0 8px 0 color-mix(in srgb, var(--stats-shelf) 72%, transparent), 0 13px 24px var(--stats-shadow);
}

.stats-line {
  position: absolute;
  right: 0;
  bottom: 1.55rem;
  left: 0;
  height: 1px;
  background: var(--stats-rule);
}

.stats-progress {
  display: block;
  width: 100%;
  height: 100%;
  transform-origin: left center;
  background: var(--color-accent);
  box-shadow: 0 0 12px color-mix(in srgb, var(--color-accent) 35%, transparent);
}

.stat-volume {
  --volume-bg: var(--stats-volume-1);
  --volume-ink: var(--stats-volume-1-ink);
  position: relative;
  display: flex;
  min-height: 18rem;
  flex-direction: column;
  overflow: visible;
  border: 1px solid color-mix(in srgb, var(--volume-ink) 22%, transparent);
  border-radius: 0.35rem 0.65rem 0.2rem 0.2rem;
  background-color: var(--volume-bg);
  background-image: linear-gradient(90deg, rgb(20 21 26 / 0.18), transparent 7%, transparent 94%, rgb(20 21 26 / 0.2));
  padding: clamp(1.2rem, 2.8vw, 2rem);
  color: var(--volume-ink);
  box-shadow: inset 5px 0 rgb(20 21 26 / 0.12), inset -3px 0 rgb(20 21 26 / 0.09), 0 8px 20px var(--stats-shadow);
  transition: transform 420ms var(--ease-out), box-shadow 220ms ease;
}

.stat-volume:nth-of-type(2) { min-height: 20rem; --volume-bg: var(--stats-volume-2); --volume-ink: var(--stats-volume-2-ink); }
.stat-volume:nth-of-type(3) { min-height: 17rem; --volume-bg: var(--stats-volume-3); --volume-ink: var(--stats-volume-3-ink); }
.stat-volume:hover { transform: translateY(-5px); box-shadow: inset 5px 0 rgb(20 21 26 / 0.16), inset -3px 0 rgb(20 21 26 / 0.12), 0 15px 30px rgb(0 0 0 / 0.3); }

.stat-node {
  position: absolute;
  bottom: -2.7rem;
  left: 50%;
  width: 0.68rem;
  height: 0.68rem;
  transform: translateX(-50%);
  border: 2px solid var(--stats-bg);
  border-radius: 999px;
  background: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--stats-ink) 18%, transparent);
}

.stat-volume-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid currentColor;
  opacity: 0.78;
}

.stat-code,
.stat-detail {
  font-family: var(--font-mono);
  font-size: 0.58rem;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

.stat-icon { width: 1.2rem; height: 1.2rem; stroke: currentColor; stroke-width: 1.35; }
.stat-number-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-top: 1.2rem; }

.stat-number {
  font-family: var(--font-display);
  font-size: clamp(4.5rem, 8vw, 7rem);
  font-weight: 400;
  line-height: 0.8;
  letter-spacing: -0.055em;
  font-variant-numeric: tabular-nums;
}

.stat-seal {
  display: grid;
  width: 3rem;
  height: 3rem;
  place-items: center;
  transform: rotate(-7deg);
  border: 1px solid currentColor;
  border-radius: 999px;
  font-family: var(--font-mono);
  font-size: 0.43rem;
  line-height: 1.2;
  text-align: center;
  text-transform: uppercase;
  opacity: 0.58;
}

.stat-copy { margin-top: auto; padding-top: 2rem; }
.stat-label { font-family: var(--font-display); font-size: clamp(1.7rem, 3vw, 2.45rem); line-height: 1; }
.stat-description { margin-top: 0.45rem; font-size: 0.75rem; opacity: 0.72; }
.stat-detail { margin-top: 1.2rem; padding-top: 0.75rem; border-top: 1px solid currentColor; opacity: 0.52; }

.editorial-section {
  --editorial-wash: rgb(227 213 193 / 0.76);
  background-color: var(--color-paper);
  background-image: linear-gradient(var(--editorial-wash), var(--editorial-wash)), var(--editorial-background);
  background-position: center;
  background-size: cover;
  border-block: 1px solid color-mix(in srgb, var(--color-rule) 48%, transparent);
}

:global(:root[data-theme='dark']) .editorial-section { --editorial-wash: rgb(108 74 60 / 0.72); }

@media (prefers-color-scheme: dark) {
  :global(:root:not([data-theme])) .editorial-section { --editorial-wash: rgb(108 74 60 / 0.72); }
}

.edition-rail {
  position: relative;
  display: grid;
  grid-auto-columns: minmax(14.5rem, 17rem);
  grid-auto-flow: column;
  gap: clamp(1rem, 2.5vw, 1.75rem);
  margin-inline: calc((100vw - min(100vw - 2rem, 72rem)) / -2);
  padding: 0.5rem max(1rem, calc((100vw - 72rem) / 2)) 1.5rem;
  overflow-x: auto;
  overscroll-behavior-inline: contain;
  scrollbar-width: none;
}

.edition-rail::-webkit-scrollbar { display: none; }
.edition-item { user-select: none; }
.edition-item:nth-child(3n + 1) :deep(.editorial-cover) { transform: rotate(-0.7deg); }
.edition-item:nth-child(3n + 2) :deep(.editorial-cover) { transform: rotate(0.8deg); }
.edition-item :deep(.editorial-cover) { transition: transform 420ms var(--ease-out), box-shadow 220ms ease; }
.edition-item:hover :deep(.editorial-cover) { transform: translateY(-6px) rotate(0deg); box-shadow: 0 14px 30px rgb(20 21 26 / 0.18); }

.authors-section {
  background-color: color-mix(in srgb, var(--color-paper-2) 78%, var(--color-paper));
  background-image: repeating-linear-gradient(
    to bottom,
    transparent 0,
    transparent calc(1.8rem - 1px),
    color-mix(in srgb, var(--color-rule) 11%, transparent) calc(1.8rem - 1px),
    color-mix(in srgb, var(--color-rule) 11%, transparent) 1.8rem
  );
}

.author-grid {
  display: grid;
  grid-auto-columns: min(86vw, 25rem);
  grid-auto-flow: column;
  gap: 1rem;
  margin-inline: -0.75rem;
  padding: 0.25rem 0.75rem 1.4rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}

.author-grid::-webkit-scrollbar { display: none; }

.author-card {
  position: relative;
  isolation: isolate;
  min-height: 31rem;
  overflow: hidden;
  scroll-snap-align: center;
  border: 1px solid color-mix(in srgb, var(--color-rule) 72%, transparent);
  border-radius: var(--radius-lg);
  background: color-mix(in srgb, var(--color-paper) 94%, var(--color-5) 6%);
  box-shadow: var(--shadow-whisper);
  color: var(--color-ink);
  transition: transform 420ms var(--ease-out), border-color 220ms ease, box-shadow 220ms ease;
}

.author-card::after {
  position: absolute;
  inset: 0;
  z-index: -1;
  background: linear-gradient(110deg, color-mix(in srgb, var(--color-paper) 97%, transparent) 22%, transparent 72%);
  content: '';
  pointer-events: none;
}

.author-card:hover,
.author-card:focus-visible {
  transform: translateY(-5px);
  border-color: color-mix(in srgb, var(--color-accent) 55%, var(--color-rule));
  box-shadow: 0 18px 40px rgb(20 21 26 / 0.14);
  outline: none;
}

.author-tab {
  position: absolute;
  top: 0;
  right: clamp(1rem, 3vw, 1.75rem);
  z-index: 4;
  padding: 0.42rem 0.75rem 0.5rem;
  background: var(--color-5);
  color: var(--color-1);
  font-family: var(--font-mono);
  font-size: 0.58rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.author-portrait {
  position: absolute;
  inset: 0 0 0 auto;
  z-index: -2;
  width: 74%;
  opacity: 0.42;
  mask-image: linear-gradient(to left, #000 32%, rgb(0 0 0 / 0.82) 58%, transparent 96%);
}

.author-portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 50% 20%;
  filter: saturate(0.72) contrast(1.04) sepia(0.18);
  transition: transform 700ms var(--ease-out), filter 420ms ease;
}

.author-card:hover .author-portrait img { transform: scale(1.025); filter: saturate(0.88) contrast(1.06) sepia(0.1); }

.author-content {
  position: relative;
  z-index: 2;
  display: flex;
  min-height: inherit;
  flex-direction: column;
  align-items: flex-start;
  padding: clamp(1.35rem, 3vw, 2.25rem);
}

.author-code {
  font-family: var(--font-mono);
  font-size: 0.66rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: var(--color-accent);
}

.author-biography,
.author-note,
.author-facts { max-width: 70%; }

.author-note {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

.author-facts span + span::before {
  margin-right: 1.25rem;
  color: var(--color-accent);
  content: '·';
}

.author-cta span { transition: transform 220ms var(--ease-out); }
.author-card:hover .author-cta span { transform: translateX(5px); }

.author-edition {
  position: absolute;
  right: 1.15rem;
  bottom: 1.15rem;
  z-index: 3;
  width: 4.6rem;
  transform: rotate(2.2deg);
  filter: saturate(0.82);
  transition: transform 420ms var(--ease-out);
}

.author-edition :deep(.editorial-cover) { box-shadow: 0 8px 18px rgb(20 21 26 / 0.2); }
.author-card:hover .author-edition { transform: translateY(-4px) rotate(0deg); }

.author-bookplate {
  display: flex;
  aspect-ratio: 2 / 3;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid color-mix(in srgb, var(--color-1) 30%, transparent);
  background: var(--color-5);
  padding: 0.65rem 0.5rem;
  color: var(--color-1);
  box-shadow: inset 3px 0 rgb(20 21 26 / 0.16), 0 8px 18px rgb(20 21 26 / 0.2);
}

.author-bookplate span {
  font-family: var(--font-mono);
  font-size: 0.42rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.author-bookplate strong {
  font-family: var(--font-display);
  font-size: 0.78rem;
  font-weight: 400;
  line-height: 1.05;
}

:global(:root[data-theme='dark']) .author-portrait { opacity: 0.18; mix-blend-mode: luminosity; }

@media (prefers-color-scheme: dark) {
  :global(:root:not([data-theme])) .author-portrait { opacity: 0.18; mix-blend-mode: luminosity; }
}

@media (min-width: 768px) {
  .author-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-auto-columns: auto;
    grid-auto-flow: row;
    margin-inline: 0;
    padding: 0.25rem 0 1rem;
    overflow: visible;
  }

  .author-card--lead { grid-column: 1 / -1; }
}

@media (max-width: 767px) {
  .stats-heading { padding-bottom: 1.5rem; }
  .stats-shelf {
    grid-template-columns: 1fr;
    align-items: stretch;
    gap: 1rem;
    margin-top: 2rem;
    padding: 0 0 0 2.2rem;
    border-bottom: 0;
    box-shadow: none;
  }

  .stats-line {
    top: 0;
    right: auto;
    bottom: 0;
    left: 0.42rem;
    width: 1px;
    height: auto;
  }

  .stats-progress { transform-origin: center top; }
  .stat-volume,
  .stat-volume:nth-of-type(2),
  .stat-volume:nth-of-type(3) { min-height: 15rem; }
  .stat-node { top: 50%; bottom: auto; left: -2.15rem; transform: translateY(-50%); }
  .stat-number { font-size: 5rem; }
}

@media (min-width: 1024px) {
  .author-grid {
    grid-template-columns: repeat(12, minmax(0, 1fr));
    grid-template-rows: repeat(2, minmax(17.5rem, auto));
  }

  .author-card { min-height: 17.5rem; grid-column: span 5; }
  .author-card--lead { min-height: 36rem; grid-column: span 7; grid-row: span 2; }
  .author-card:not(.author-card--lead) .author-content { padding: 1.55rem; }
  .author-card:not(.author-card--lead) .author-biography { display: none; }
  .author-card:not(.author-card--lead) .author-note { max-width: 62%; margin-top: 0.85rem; font-size: 1rem; -webkit-line-clamp: 2; }
  .author-card:not(.author-card--lead) .author-facts { max-width: 68%; padding-top: 1rem; }
  .author-card:not(.author-card--lead) .author-cta { margin-top: 0.8rem; }
  .author-card:not(.author-card--lead) .author-portrait { width: 58%; opacity: 0.32; }
  .author-card--lead .author-edition { right: 1.75rem; bottom: 1.75rem; width: 5.5rem; }
}

</style>
