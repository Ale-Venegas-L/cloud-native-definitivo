<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'

interface Props {
  open: boolean
  title?: string
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  maxWidth: 'md'
})

const emit = defineEmits<{
  close: []
}>()

const dialogEl = ref<HTMLDialogElement | null>(null)

const maxWidthClasses: Record<string, string> = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-xl'
}

watch(() => props.open, (isOpen) => {
  if (!dialogEl.value) return
  if (isOpen) {
    dialogEl.value.showModal()
    document.body.style.overflow = 'hidden'
  } else {
    dialogEl.value.close()
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  if (props.open && dialogEl.value) {
    dialogEl.value.showModal()
    document.body.style.overflow = 'hidden'
  }
})

onUnmounted(() => {
  document.body.style.overflow = ''
})

function onBackdropClick(e: MouseEvent) {
  if (e.target === dialogEl.value) {
    emit('close')
  }
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    emit('close')
  }
}
</script>

<template>
  <dialog
    ref="dialogEl"
    :class="[
      'rounded-[var(--radius-xl)] p-0 bg-transparent backdrop:bg-ink/40',
      'backdrop:transition-opacity backdrop:duration-[var(--dur-long)]',
      maxWidthClasses[maxWidth],
      'w-full'
    ]"
    @click="onBackdropClick"
    @keydown="onKeydown"
  >
    <div
      v-if="open"
      class="bg-paper rounded-[var(--radius-xl)] shadow-[var(--shadow-card)] overflow-hidden
             animate-[modalIn_var(--dur-long)_var(--ease-out)]"
    >
      <div v-if="title" class="flex items-center justify-between px-6 py-4 border-b border-rule">
        <h3 class="text-xl font-[var(--font-display)] text-ink">{{ title }}</h3>
        <button
          class="p-1.5 rounded-[var(--radius-sm)] text-ink-3 hover:text-ink hover:bg-paper-2
                 transition-colors duration-[var(--dur-short)]"
          @click="emit('close')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="px-6 py-5">
        <slot />
      </div>
      <div v-if="$slots.footer" class="px-6 py-4 border-t border-rule bg-paper-2/50">
        <slot name="footer" />
      </div>
    </div>
  </dialog>
</template>

<style scoped>
@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(4px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
