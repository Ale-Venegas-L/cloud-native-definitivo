import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseButton from '@/components/UI/BaseButton.vue'

describe('BaseButton', () => {
  it('renders slot content', () => {
    const wrapper = mount(BaseButton, { slots: { default: 'Click me' } })
    expect(wrapper.text()).toContain('Click me')
  })

  it('applies primary variant by default', () => {
    const wrapper = mount(BaseButton, { slots: { default: 'Btn' } })
    expect(wrapper.classes()).toContain('bg-ink')
  })

  it('applies secondary variant', () => {
    const wrapper = mount(BaseButton, {
      props: { variant: 'secondary' },
      slots: { default: 'Btn' },
    })
    expect(wrapper.classes()).toContain('border')
  })

  it('applies danger variant', () => {
    const wrapper = mount(BaseButton, {
      props: { variant: 'danger' },
      slots: { default: 'Btn' },
    })
    expect(wrapper.classes()).toContain('bg-danger')
  })

  it('applies ghost variant', () => {
    const wrapper = mount(BaseButton, {
      props: { variant: 'ghost' },
      slots: { default: 'Btn' },
    })
    expect(wrapper.classes()).toContain('bg-transparent')
  })

  it('applies sm size', () => {
    const wrapper = mount(BaseButton, {
      props: { size: 'sm' },
      slots: { default: 'Btn' },
    })
    expect(wrapper.classes()).toContain('px-3')
  })

  it('applies lg size', () => {
    const wrapper = mount(BaseButton, {
      props: { size: 'lg' },
      slots: { default: 'Btn' },
    })
    expect(wrapper.classes()).toContain('px-7')
  })

  it('is disabled when disabled prop is true', async () => {
    const wrapper = mount(BaseButton, {
      props: { disabled: true },
      slots: { default: 'Btn' },
    })
    expect(wrapper.attributes('disabled')).toBeDefined()
  })

  it('is disabled when loading', async () => {
    const wrapper = mount(BaseButton, {
      props: { loading: true },
      slots: { default: 'Btn' },
    })
    expect(wrapper.attributes('disabled')).toBeDefined()
  })

  it('shows spinner when loading', () => {
    const wrapper = mount(BaseButton, {
      props: { loading: true },
      slots: { default: 'Btn' },
    })
    expect(wrapper.find('svg.animate-spin').exists()).toBe(true)
  })
})
