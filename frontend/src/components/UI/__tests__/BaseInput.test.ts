import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseInput from '@/components/UI/BaseInput.vue'

describe('BaseInput', () => {
  it('renders with label', () => {
    const wrapper = mount(BaseInput, { props: { label: 'Nombre' } })
    expect(wrapper.text()).toContain('Nombre')
  })

  it('renders placeholder', () => {
    const wrapper = mount(BaseInput, { props: { placeholder: 'Escribe aqui' } })
    expect(wrapper.find('input').attributes('placeholder')).toBe('Escribe aqui')
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(BaseInput, { props: { modelValue: '' } })
    await wrapper.find('input').setValue('test')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')![0]).toEqual(['test'])
  })

  it('emits number value for number type', async () => {
    const wrapper = mount(BaseInput, {
      props: { modelValue: 0, type: 'number' },
    })
    await wrapper.find('input').setValue('42')
    expect(wrapper.emitted('update:modelValue')![0]).toEqual([42])
  })

  it('shows error message', () => {
    const wrapper = mount(BaseInput, { props: { error: 'Campo requerido' } })
    expect(wrapper.text()).toContain('Campo requerido')
  })

  it('applies danger class when error', () => {
    const wrapper = mount(BaseInput, { props: { error: 'Error' } })
    expect(wrapper.find('input').classes()).toContain('border-danger')
  })

  it('disables input when disabled prop is true', () => {
    const wrapper = mount(BaseInput, { props: { disabled: true } })
    expect(wrapper.find('input').attributes('disabled')).toBeDefined()
  })

  it('does not render label when not provided', () => {
    const wrapper = mount(BaseInput)
    expect(wrapper.find('label').exists()).toBe(false)
  })
})
