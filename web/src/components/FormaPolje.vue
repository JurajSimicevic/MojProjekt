<script setup lang="ts">
defineProps<{
  oznaka: string
  modelValue: string | number
  vrsta?: string
  greska?: string
  obavezno?: boolean
  pomoc?: string
}>()

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <div class="polje">
    <label :for="oznaka">
      {{ oznaka }}<span v-if="obavezno" class="obavezno">*</span>
    </label>
    <input
      :id="oznaka"
      :type="vrsta ?? 'text'"
      :value="modelValue"
      :required="obavezno"
      :class="{ 'input--greska': greska }"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <span v-if="greska" class="greska-tekst">{{ greska }}</span>
    <span v-else-if="pomoc" class="pomoc-tekst">{{ pomoc }}</span>
  </div>
</template>

<style scoped>
.polje { display: flex; flex-direction: column; gap: 0.6rem; }

label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--boja-tekst);
  letter-spacing: 0;
}

.obavezno { color: var(--boja-akcent); margin-left: 0.2rem; }

input {
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.875rem 1rem;
  border-radius: 8px;
  font-size: 1rem;
  transition: all var(--tranzicija);
}

input:focus { outline: none; border-color: var(--boja-akcent); box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.1); }
input.input--greska { border-color: var(--boja-opasnost); }

.greska-tekst { font-size: 0.85rem; color: var(--boja-opasnost); }
.pomoc-tekst  { font-size: 0.85rem; color: var(--boja-tekst-mute); }
</style>
