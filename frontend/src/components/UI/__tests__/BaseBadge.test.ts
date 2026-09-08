import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseBadge from '@/components/UI/BaseBadge.vue'

describe('BaseBadge', () => {
  it('renders slot content', () => {
    const wrapper = mount(BaseBadge, { slots: { default: 'Nuevo' } })
    expect(wrapper.text()).toContain('Nuevo')
  })

  it('applies default variant', () => {
    const wrapper = mount(BaseBadge, { slots: { default: 'Tag' } })
    expect(wrapper.classes()).toContain('bg-paper-2')
  })

  it('applies accent variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'accent' },
      slots: { default: 'Tag' },
    })
    expect(wrapper.classes()).toContain('bg-accent/10')
  })

  it('applies danger variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'danger' },
      slots: { default: 'Tag' },
    })
    expect(wrapper.classes()).toContain('bg-danger/10')
  })

  it('applies success variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'success' },
      slots: { default: 'Tag' },
    })
    expect(wrapper.classes()).toContain('bg-green-500/10')
  })
})
