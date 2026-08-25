<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import libraryImage from '../../assets/img/hero/libreria-footer.webp'

const footerEl = ref<HTMLElement | null>(null)
const isRevealed = ref(false)
let observer: IntersectionObserver | null = null
let frameId: number | null = null

function reveal(): void {
  if (isRevealed.value) return
  isRevealed.value = true
  observer?.disconnect()
  window.removeEventListener('scroll', scheduleCheck)
  window.removeEventListener('resize', scheduleCheck)
}

function checkPosition(): void {
  frameId = null
  if (!footerEl.value || isRevealed.value) return
  const rect = footerEl.value.getBoundingClientRect()
  if (rect.top <= window.innerHeight * 0.92 && rect.bottom >= 0) reveal()
}

function scheduleCheck(): void {
  if (frameId !== null || isRevealed.value) return
  frameId = window.requestAnimationFrame(checkPosition)
}

onMounted(() => {
  if (!footerEl.value) return

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    reveal()
    return
  }

  observer = new IntersectionObserver(([entry]) => {
    if (entry?.isIntersecting) reveal()
  }, { threshold: 0.01, rootMargin: '0px 0px 10% 0px' })

  observer.observe(footerEl.value)
  window.addEventListener('scroll', scheduleCheck, { passive: true })
  window.addEventListener('resize', scheduleCheck, { passive: true })
  checkPosition()
})

onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('scroll', scheduleCheck)
  window.removeEventListener('resize', scheduleCheck)
  if (frameId !== null) window.cancelAnimationFrame(frameId)
})
</script>

<template>
  <footer ref="footerEl" :class="['library-footer', { 'library-footer--revealed': isRevealed }]">
    <img :src="libraryImage" alt="" aria-hidden="true" class="footer-library" width="1672" height="941" decoding="async" fetchpriority="low">
    <div class="footer-image-shadow" aria-hidden="true" />

    <div class="footer-content page-shell">
      <div class="footer-copy">
        <p class="footer-eyebrow">Classic Library</p>
        <h2 class="footer-title">Toda gran lectura comienza con una página.</h2>
        <p class="footer-description">Recorre nuestra selección de obras esenciales y encuentra la próxima historia que permanecerá contigo.</p>
        <router-link to="/books" class="footer-cta">Explorar la colección <span aria-hidden="true">→</span></router-link>
      </div>

      <div class="footer-meta">
        <p>© 2026 Classic Library</p>
        <nav aria-label="Navegación del pie de página">
          <router-link to="/">Inicio</router-link>
          <router-link to="/books">Catálogo</router-link>
          <router-link to="/login">Administración</router-link>
        </nav>
      </div>
    </div>

  </footer>
</template>

<style scoped>
.library-footer {
  position: relative;
  isolation: isolate;
  min-height: clamp(34rem, 68vw, 48rem);
  overflow: hidden;
  border-top: 1px solid #8D806F;
  background-color: #E3D5C1;
  background-image:
    radial-gradient(circle at 16% 12%, rgb(138 99 74 / 0.11), transparent 28%),
    radial-gradient(circle at 84% 38%, rgb(175 178 180 / 0.13), transparent 34%),
    linear-gradient(90deg, transparent 0, transparent 8.5%, rgb(138 99 74 / 0.3) 8.5%, rgb(138 99 74 / 0.3) calc(8.5% + 1px), transparent calc(8.5% + 1px)),
    repeating-linear-gradient(to bottom, transparent 0, transparent 31px, rgb(141 128 111 / 0.34) 31px, rgb(141 128 111 / 0.34) 32px);
  color: #14151A;
}

.footer-content {
  position: relative;
  z-index: 3;
  display: flex;
  min-height: clamp(34rem, 68vw, 48rem);
  flex-direction: column;
  padding-top: clamp(4rem, 8vw, 5rem);
  padding-bottom: 1.75rem;
  text-align: center;
}

.footer-copy {
  max-width: 42rem;
  margin-inline: auto;
  transform: translate3d(0, 12px, 0);
  transition: transform 900ms cubic-bezier(0.16, 1, 0.3, 1);
  color: #14151A;
  mix-blend-mode: multiply;
}

.footer-eyebrow {
  margin: 0 auto 1rem;
  color: var(--color-accent-2);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.footer-title {
  color: rgb(20 21 26 / 0.94);
  font-size: clamp(2.6rem, 6vw, 5rem);
  line-height: 0.96;
  text-shadow: 0 0 0.45px rgb(20 21 26 / 0.5);
}

.footer-description {
  max-width: 32rem;
  margin: 1.25rem auto 0;
  color: rgb(20 21 26 / 0.74);
  font-size: clamp(0.875rem, 1.4vw, 1rem);
}

.footer-cta {
  display: inline-flex;
  min-height: 3rem;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.75rem;
  padding-inline: 1.5rem;
  border: 1px solid rgb(20 21 26 / 0.34);
  border-radius: 0.5rem;
  background: transparent;
  color: #14151A;
  font-size: 0.875rem;
  font-weight: 500;
  backdrop-filter: blur(8px);
  box-shadow: inset 0 0 0 1px rgb(138 99 74 / 0.08);
  transition: transform 220ms ease, background-color 220ms ease, color 220ms ease;
}

.footer-cta:hover {
  transform: translateY(-2px);
  background: #14151A;
  color: #E3D5C1;
}

.footer-meta {
  position: relative;
  z-index: 4;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: auto;
  padding-top: 1.25rem;
  border-top: 1px solid rgb(227 213 193 / 0.22);
  color: rgb(227 213 193 / 0.72);
  font-size: 0.75rem;
}

.footer-meta nav {
  display: flex;
  gap: 1.25rem;
}

.footer-meta a {
  color: rgb(227 213 193 / 0.82);
}

.footer-meta a:hover {
  color: #E3D5C1;
}

.footer-library {
  position: absolute;
  z-index: 1;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center bottom;
  pointer-events: none;
  user-select: none;
  opacity: 0.82;
  transform: translate3d(0, 18%, 0) scale(1.025);
  transform-origin: 50% 100%;
  transition: transform 1400ms cubic-bezier(0.16, 1, 0.3, 1), opacity 900ms ease;
  will-change: transform, opacity;
  filter: drop-shadow(0 -24px 34px rgb(20 21 26 / 0.72));
}

.footer-image-shadow {
  position: absolute;
  z-index: 2;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(180deg, transparent 0%, transparent 38%, rgb(20 21 26 / 0.08) 56%, rgb(20 21 26 / 0.52) 100%);
  box-shadow: inset 0 -42px 80px rgb(20 21 26 / 0.34);
}

.library-footer--revealed .footer-copy {
  transform: translate3d(0, 0, 0);
}

.library-footer--revealed .footer-library {
  opacity: 1;
  transform: translate3d(0, 0, 0) scale(1);
}

@media (max-width: 639px) {
  .footer-meta {
    flex-direction: column;
  }

  .footer-library {
    object-position: 52% bottom;
    transform: translate3d(0, 14%, 0) scale(1.02);
  }
}

@media (prefers-reduced-motion: reduce) {
  .footer-copy,
  .footer-library {
    transition: none;
    transform: none;
    opacity: 1;
  }
}
</style>
