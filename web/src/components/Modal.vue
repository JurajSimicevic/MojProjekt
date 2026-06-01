<script setup lang="ts">
defineProps<{
  modelValue: boolean
  naslov: string
}>()

const emit = defineEmits<{
  'update:modelValue': [v: boolean]
}>()
</script>

<template>
  <Teleport to="body">
    <div v-if="modelValue" class="overlay" @click.self="emit('update:modelValue', false)">
      <div class="modal" role="dialog" :aria-label="naslov">
        <div class="modal-zaglavlje">
          <h2 class="modal-naslov">{{ naslov }}</h2>
          <button class="zatvori" @click="emit('update:modelValue', false)">×</button>
        </div>
        <div class="modal-sadrzaj">
          <slot />
        </div>
        <div v-if="$slots['akcije']" class="modal-akcije">
          <slot name="akcije" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: var(--boja-pozadina);
  width: min(480px, 90vw);
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  animation: modalSlideIn var(--tranzicija);
}

@keyframes modalSlideIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-zaglavlje {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: none;
}

.modal-naslov {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: 0;
}

.zatvori {
  font-size: 1.5rem;
  color: var(--boja-tekst-mute);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all var(--tranzicija);
}

.zatvori:hover { color: var(--boja-tekst); background: var(--boja-povrsina); }

.modal-sadrzaj {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.modal-akcije {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid var(--boja-rub);
}
</style>
