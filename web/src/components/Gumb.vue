<script setup lang="ts">
defineProps<{
  vrsta?: 'primarni' | 'sekundarni' | 'opasnost'
  velicina?: 'mali' | 'normalni'
  ucitava?: boolean
  onemoguceno?: boolean
  tip?: 'button' | 'submit' | 'reset'
}>()
</script>

<template>
  <button
    :type="tip ?? 'button'"
    :disabled="onemoguceno || ucitava"
    :class="['gumb', `gumb--${vrsta ?? 'primarni'}`, `gumb--${velicina ?? 'normalni'}`]"
  >
    <slot>{{ ucitava ? 'Učitavanje...' : '' }}</slot>
  </button>
</template>

<style scoped>
.gumb {
  font-family: var(--font-body);
  font-weight: 600;
  cursor: pointer;
  border: none;
  border-radius: 8px;
  transition: all var(--tranzicija);
  font-size: 1rem;
  letter-spacing: 0;
}

.gumb:disabled { opacity: 0.5; cursor: not-allowed; }

.gumb--normalni { padding: 0.875rem 1.5rem; }
.gumb--mali    { padding: 0.5rem 1rem; font-size: 0.875rem; }

.gumb--primarni { background: var(--boja-akcent); color: white; box-shadow: var(--sjena); }
.gumb--primarni:hover:not(:disabled) { background: var(--boja-akcent-tamno); box-shadow: var(--sjena-lg); transform: translateY(-1px); }

.gumb--sekundarni { background: transparent; color: var(--boja-tekst-mute); border: 1px solid var(--boja-rub); }
.gumb--sekundarni:hover:not(:disabled) { color: var(--boja-tekst); border-color: var(--boja-akcent); background: var(--boja-povrsina); }

.gumb--opasnost { background: transparent; color: var(--boja-opasnost); border: 1px solid var(--boja-opasnost); }
.gumb--opasnost:hover:not(:disabled) { background: var(--boja-opasnost); color: white; }
</style>
