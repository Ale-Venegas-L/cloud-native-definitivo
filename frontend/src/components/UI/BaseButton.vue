<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false
})

const variantClasses: Record<string, string> = {
  primary: 'bg-ink text-paper hover:bg-ink/90 active:bg-ink/80',
  secondary: 'bg-transparent text-ink border border-rule hover:bg-paper-2 active:bg-paper-3',
  danger: 'bg-danger text-[#E3D5C1] hover:opacity-90 active:opacity-80',
  ghost: 'bg-transparent text-ink-2 hover:bg-paper-2 active:bg-paper-3'
}

const sizeClasses: Record<string, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-5 py-2.5 text-base',
  lg: 'px-7 py-3 text-lg'
}
</script>

<template>
  <button
    :class="[
      'inline-flex min-h-11 items-center justify-center gap-2 rounded-[var(--radius-md)] font-medium',
      'transition-[transform,opacity] duration-[var(--dur-short)] ease-[var(--ease-out)]',
      'focus-visible:outline-2 focus-visible:outline-offset-3 focus-visible:outline-focus',
      'disabled:opacity-40 disabled:pointer-events-none',
      variantClasses[props.variant],
      sizeClasses[props.size]
    ]"
    :disabled="disabled || loading"
    :aria-busy="loading"
  >
    <svg v-if="loading" class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <slot />
  </button>
</template>
