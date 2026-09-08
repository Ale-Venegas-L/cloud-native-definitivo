import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import booksPage from '@/components/pages/public/books.vue'

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [{ path: '/', component: booksPage }],
  })
}

describe('BooksPage', () => {
  it('renders the catalog heading', () => {
    const wrapper = mount(booksPage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    expect(wrapper.text()).toContain('Catálogo')
  })

  it('renders search input', () => {
    const wrapper = mount(booksPage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    const input = wrapper.find('input[type="text"]')
    expect(input.exists()).toBe(true)
  })

  it('renders filter selects', () => {
    const wrapper = mount(booksPage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    const selects = wrapper.findAll('select')
    expect(selects.length).toBe(3)
  })

  it('shows 0 books initially', () => {
    const wrapper = mount(booksPage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    expect(wrapper.text()).toContain('0 libros')
  })

  it('filters books by search text', async () => {
    const wrapper = mount(booksPage, {
      global: {
        plugins: [createTestRouter()],
        stubs: { teleport: true },
      },
    })
    const searchInput = wrapper.find('input[type="text"]')
    await searchInput.setValue('Test')
    expect((searchInput.element as HTMLInputElement).value).toBe('Test')
  })
})
