<script setup lang="ts">
interface Props {
  variant?: 'default' | 'elevated' | 'outlined'
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  padding: 'md'
})

const variantClasses: Record<string, string> = {
  default: 'bg-paper-2 border border-rule',
  elevated: 'bg-paper-2 shadow-[var(--shadow-card)]',
  outlined: 'bg-transparent border border-rule'
}

const paddingClasses: Record<string, string> = {
  none: '',
  sm: 'p-3',
  md: 'p-5',
  lg: 'p-7'
}
</script>

<template>
  <div
    :class="[
      'rounded-[var(--radius-lg)] transition-all duration-[var(--dur-short)] ease-[var(--ease-out)]',
      variantClasses[props.variant],
      paddingClasses[props.padding]
    ]"
  >
    <slot />
  </div>
</template>
