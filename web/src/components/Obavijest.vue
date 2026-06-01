<script setup lang="ts">
import type { Obavijest } from '@/stores/obavijesti'
import { useObavijestiStore } from '@/stores/obavijesti'

const props = defineProps<{ obavijest: Obavijest }>()
const store = useObavijestiStore()
</script>

<template>
  <div
    :class="['obavijest', `obavijest--${props.obavijest.vrsta}`]"
    @click="store.ukloni(props.obavijest.id)"
  >
    <span class="poruka">{{ props.obavijest.poruka }}</span>
    <button class="zatvori" aria-label="Zatvori">×</button>
  </div>
</template>

<style scoped>
.obavijest {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  min-width: 300px;
  max-width: 450px;
  box-shadow: var(--sjena-lg);
  border: 1px solid transparent;
  animation: slideIn var(--tranzicija);
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.obavijest--uspjeh {
  border-color: var(--boja-uspjeh);
  color: var(--boja-uspjeh);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, transparent 100%);
}

.obavijest--greska {
  border-color: var(--boja-opasnost);
  color: var(--boja-opasnost);
  background: linear-gradient(135deg, rgba(255, 82, 82, 0.05) 0%, transparent 100%);
}

.obavijest--info {
  border-color: var(--boja-tekst-mute);
  color: var(--boja-tekst);
}

.poruka {
  font-size: 0.95rem;
  line-height: 1.5;
  font-weight: 500;
}

.zatvori {
  font-size: 1.5rem;
  color: inherit;
  opacity: 0.6;
  flex-shrink: 0;
  transition: opacity var(--tranzicija);
}

.zatvori:hover {
  opacity: 1;
}
</style>
