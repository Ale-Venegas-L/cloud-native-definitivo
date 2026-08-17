import { onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'

export function useScrollReveal(selector: string = '.reveal') {
  let observer: IntersectionObserver | null = null

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  onMounted(() => {
    if (prefersReducedMotion) {
      document.querySelectorAll(selector).forEach((el) => {
        el.classList.add('is-visible')
      })
      return
    }

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target as HTMLElement
            const delay = parseInt(el.dataset.revealDelay || '0', 10)

            gsap.fromTo(
              el,
              { opacity: 0, y: 12 },
              {
                opacity: 1,
                y: 0,
                duration: 0.42,
                delay: delay * 0.06,
                ease: 'power3.out',
                onComplete: () => {
                  el.classList.add('is-visible')
                }
              }
            )

            observer?.unobserve(el)
          }
        })
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    )

    document.querySelectorAll(selector).forEach((el, index) => {
      el.setAttribute('data-reveal-delay', String(index))
      observer!.observe(el)
    })
  })

  onUnmounted(() => {
    observer?.disconnect()
  })
}
