import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseModal from '@/components/UI/BaseModal.vue'

describe('BaseModal', () => {
  beforeEach(() => {
    HTMLDialogElement.prototype.showModal = vi.fn()
    HTMLDialogElement.prototype.close = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders title when provided', () => {
    const wrapper = mount(BaseModal, {
      props: { open: true, title: 'Mi modal' },
      slots: { default: 'Content' },
    })
    expect(wrapper.text()).toContain('Mi modal')
  })

  it('renders slot content', () => {
    const wrapper = mount(BaseModal, {
      props: { open: true },
      slots: { default: 'Modal body' },
    })
    expect(wrapper.text()).toContain('Modal body')
  })

  it('emits close on backdrop click', async () => {
    const wrapper = mount(BaseModal, {
      props: { open: true },
      slots: { default: 'Content' },
    })
    const dialog = wrapper.find('dialog')
    await dialog.trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('emits close on close button click', async () => {
    const wrapper = mount(BaseModal, {
      props: { open: true, title: 'Title' },
      slots: { default: 'Content' },
    })
    const closeBtn = wrapper.find('button')
    await closeBtn.trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('does not render title when not provided', () => {
    const wrapper = mount(BaseModal, {
      props: { open: true },
      slots: { default: 'Content' },
    })
    expect(wrapper.find('h3').exists()).toBe(false)
  })
})
