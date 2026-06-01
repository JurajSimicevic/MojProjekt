<script setup lang="ts" generic="T extends Record<string, unknown>">
defineProps<{
  stupci: { kljuc: string; oznaka: string }[]
  redovi: T[]
  stanje: 'ucitavanje' | 'greska' | 'prazno' | 'spremno'
  porukaPrazno?: string
  porukaGreske?: string
}>()
</script>

<template>
  <div>
    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">
      {{ porukaGreske ?? 'Greška pri dohvatu podataka.' }}
    </div>
    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">
      {{ porukaPrazno ?? 'Nema podataka.' }}
    </div>
    <table v-else class="tablica">
      <thead>
        <tr>
          <th v-for="s in stupci" :key="s.kljuc">{{ s.oznaka }}</th>
          <th v-if="$slots['akcije']"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(red, i) in redovi" :key="i">
          <td v-for="s in stupci" :key="s.kljuc">{{ red[s.kljuc] }}</td>
          <td v-if="$slots['akcije']" class="akcije-celija">
            <slot name="akcije" :red="red" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.stanje-poruka {
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--boja-rub);
  font-size: 0.95rem;
  text-align: center;
}

.stanje-poruka.greska {
  border-color: var(--boja-opasnost);
  color: var(--boja-opasnost);
  background: rgba(255, 82, 82, 0.05);
}

.tablica {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.tablica th {
  text-align: left;
  padding: 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--boja-tekst);
  border-bottom: 2px solid var(--boja-rub);
  background: var(--boja-povrsina);
}

.tablica td {
  padding: 1rem;
  border-bottom: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
}

.tablica tbody tr:hover td {
  background: var(--boja-povrsina);
}

.akcije-celija {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}
</style>
