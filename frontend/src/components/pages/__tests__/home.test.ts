import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import homePage from '@/components/pages/public/home.vue'

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [{ path: '/', component: homePage }],
  })
}

describe('HomePage', () => {
  it('renders the hero section', () => {
    const wrapper = mount(homePage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    expect(wrapper.text()).toContain('Biblioteca de literatura clásica')
  })

  it('renders the explore link', () => {
    const wrapper = mount(homePage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    expect(wrapper.text()).toContain('Explorar catálogo')
  })

  it('renders stats section', () => {
    const wrapper = mount(homePage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    expect(wrapper.text()).toContain('Libros')
    expect(wrapper.text()).toContain('Autores')
    expect(wrapper.text()).toContain('Países')
  })

  it('renders featured authors section', () => {
    const wrapper = mount(homePage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    expect(wrapper.text()).toContain('Autores destacados')
    expect(wrapper.text()).toContain('Miguel de Cervantes')
    expect(wrapper.text()).toContain('Gabriel García Márquez')
    expect(wrapper.text()).toContain('William Shakespeare')
  })
})
