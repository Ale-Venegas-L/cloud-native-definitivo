<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const progress = ref(0)
const offset = ref(0)
const isScrollable = ref(false)
const isScrolling = ref(false)
let frameId: number | null = null
let resizeObserver: ResizeObserver | null = null
let hideTimer: ReturnType<typeof window.setTimeout> | null = null

const percentage = computed(() => Math.round(progress.value * 100))
const isVisible = computed(() => isScrollable.value && isScrolling.value && progress.value > 0.018 && progress.value < 0.982)

function updatePosition(): void {
  frameId = null
  const root = document.documentElement
  const scrollable = Math.max(0, root.scrollHeight - window.innerHeight)
  isScrollable.value = scrollable > 1
  progress.value = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0

  const topSpace = window.innerWidth < 640 ? 76 : 88
  const bottomSpace = 28
  const markerHeight = window.innerWidth < 640 ? 24 : 28
  const available = Math.max(0, window.innerHeight - topSpace - bottomSpace - markerHeight)
  offset.value = progress.value * available
}

function scheduleUpdate(): void {
  if (frameId !== null) return
  frameId = window.requestAnimationFrame(updatePosition)
}

function onScroll(): void {
  isScrolling.value = true
  if (hideTimer !== null) window.clearTimeout(hideTimer)
  hideTimer = window.setTimeout(() => { isScrolling.value = false }, 850)
  scheduleUpdate()
}

onMounted(() => {
  updatePosition()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', scheduleUpdate, { passive: true })
  resizeObserver = new ResizeObserver(scheduleUpdate)
  resizeObserver.observe(document.body)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', scheduleUpdate)
  resizeObserver?.disconnect()
  if (hideTimer !== null) window.clearTimeout(hideTimer)
  if (frameId !== null) window.cancelAnimationFrame(frameId)
})
</script>

<template>
  <div
    :class="['scroll-bookmark', { 'scroll-bookmark--visible': isVisible }]"
    role="progressbar"
    aria-label="Progreso de la página"
    aria-valuemin="0"
    aria-valuemax="100"
    :aria-valuenow="percentage"
    :aria-hidden="!isVisible"
    :style="{ transform: `translate3d(0, ${offset}px, 0)` }"
  >
    <svg class="scroll-bookmark__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.7" d="M12 6.5v12m0-12C10.7 5.5 9 5 7.25 5S3.8 5.5 2.5 6.5v12c1.3-1 3-1.5 4.75-1.5S10.7 17.5 12 18.5m0-12C13.3 5.5 15 5 16.75 5s3.45.5 4.75 1.5v12c-1.3-1-3-1.5-4.75-1.5S13.3 17.5 12 18.5" />
    </svg>
  </div>
</template>

<style scoped>
.scroll-bookmark {
  position: fixed;
  z-index: 350;
  top: 5.5rem;
  right: 0;
  width: 4.75rem;
  height: 1.75rem;
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 14% 50%);
  background: linear-gradient(90deg, #8A634A 0%, var(--color-accent-2) 52%, var(--color-accent) 100%);
  box-shadow: -5px 3px 12px rgb(20 21 26 / 0.24);
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transition: transform 140ms cubic-bezier(0.22, 1, 0.36, 1), opacity 180ms ease, visibility 0s linear 180ms;
  will-change: transform;
}

.scroll-bookmark--visible {
  opacity: 1;
  visibility: visible;
  transition-delay: 0s;
}

.scroll-bookmark::after {
  position: absolute;
  inset: 2px 0 auto 0.6rem;
  height: 1px;
  content: "";
  background: rgb(227 213 193 / 0.4);
}

.scroll-bookmark__icon {
  position: absolute;
  top: 50%;
  right: 1rem;
  width: 1.15rem;
  height: 1.15rem;
  color: #E3D5C1;
  filter: drop-shadow(0 1px 2px rgb(20 21 26 / 0.34));
  transform: translateY(-50%);
}

@media (max-width: 639px) {
  .scroll-bookmark {
    top: 4.75rem;
    width: 4rem;
    height: 1.5rem;
  }

  .scroll-bookmark__icon {
    right: 0.8rem;
    width: 1rem;
    height: 1rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-bookmark {
    transition: none;
  }
}
</style>
