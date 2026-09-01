<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  modelValue?: string | number | null
  label?: string
  type?: string
  placeholder?: string
  error?: string
  disabled?: boolean
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  label: '',
  type: 'text',
  placeholder: '',
  error: '',
  disabled: false,
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
}>()

const focused = ref(false)

function onInput(e: Event) {
  const val = (e.target as HTMLInputElement).value
  emit('update:modelValue', props.type === 'number' ? (val === '' ? null : Number(val)) : val)
}
</script>

<template>
  <div class="flex flex-col gap-1.5">
    <label
      v-if="label"
      :for="`field-${String(label).toLowerCase().replaceAll(' ', '-')}`"
      :class="[
        'text-sm font-medium transition-colors duration-[var(--dur-short)]',
        focused ? 'text-accent' : 'text-ink-2'
      ]"
    >
      {{ label }}
    </label>
    <input
      :id="`field-${String(label).toLowerCase().replaceAll(' ', '-')}`"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :aria-invalid="Boolean(error)"
      :class="[
        'w-full min-h-11 px-4 py-2.5 rounded-[var(--radius-md)]',
        'bg-paper border border-rule text-ink',
        'placeholder:text-ink-3',
        'transition-[border-color,box-shadow] duration-[var(--dur-short)] ease-[var(--ease-out)]',
        'focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/20',
        'disabled:opacity-40 disabled:cursor-not-allowed',
        error ? 'border-danger' : ''
      ]"
      @input="onInput"
      @focus="focused = true"
      @blur="focused = false"
    >
    <span v-if="error" class="text-sm text-danger">{{ error }}</span>
  </div>
</template>
