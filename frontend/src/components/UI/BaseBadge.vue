<script setup lang="ts">
interface Props {
  variant?: 'default' | 'accent' | 'danger' | 'success'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
})

const variantClasses: Record<string, string> = {
  default: 'bg-paper-2 text-ink-2 border border-rule',
  accent: 'bg-accent/10 text-accent border border-accent/20',
  danger: 'bg-danger/10 text-danger border border-danger/20',
  success: 'bg-green-500/10 text-green-600 border border-green-500/20'
}
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium',
      variantClasses[props.variant]
    ]"
  >
    <slot />
  </span>
</template>
