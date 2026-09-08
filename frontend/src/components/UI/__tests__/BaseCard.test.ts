import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseCard from '@/components/UI/BaseCard.vue'

describe('BaseCard', () => {
  it('renders slot content', () => {
    const wrapper = mount(BaseCard, { slots: { default: 'Card content' } })
    expect(wrapper.text()).toContain('Card content')
  })

  it('applies default variant', () => {
    const wrapper = mount(BaseCard, { slots: { default: 'Content' } })
    expect(wrapper.classes()).toContain('bg-paper-2')
    expect(wrapper.classes()).toContain('border')
  })

  it('applies elevated variant', () => {
    const wrapper = mount(BaseCard, {
      props: { variant: 'elevated' },
      slots: { default: 'Content' },
    })
    expect(wrapper.classes()).toContain('shadow-[var(--shadow-card)]')
  })

  it('applies outlined variant', () => {
    const wrapper = mount(BaseCard, {
      props: { variant: 'outlined' },
      slots: { default: 'Content' },
    })
    expect(wrapper.classes()).toContain('border')
    expect(wrapper.classes()).toContain('bg-transparent')
  })

  it('applies md padding by default', () => {
    const wrapper = mount(BaseCard, { slots: { default: 'Content' } })
    expect(wrapper.classes()).toContain('p-5')
  })

  it('applies sm padding', () => {
    const wrapper = mount(BaseCard, {
      props: { padding: 'sm' },
      slots: { default: 'Content' },
    })
    expect(wrapper.classes()).toContain('p-3')
  })

  it('applies no padding', () => {
    const wrapper = mount(BaseCard, {
      props: { padding: 'none' },
      slots: { default: 'Content' },
    })
    expect(wrapper.classes().find((c) => c.startsWith('p-'))).toBeUndefined()
  })
})
