<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dohvatiRestorante } from '@/services/restorani'
import type { Restoran } from '@/types/restoran'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const restorani = ref<Restoran[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

async function ucitaj(): Promise<void> {
  stanje.value = 'ucitavanje'
  try {
    const podaci = await dohvatiRestorante()
    restorani.value = podaci.filter((r) => r.is_active)
    stanje.value = restorani.value.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
  }
}

onMounted(ucitaj)
</script>

<template>
  <div class="pogled">
    <h1>Restorani</h1>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">{{ porukaGreske }}</div>
    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">Nema dostupnih restorana.</div>
    <div v-else class="lista-restorana">
      <RouterLink
        v-for="r in restorani"
        :key="r.id"
        :to="`/kupac/restorani/${r.id}`"
        class="kartica-restorana"
      >
        <div class="kartica-naziv">{{ r.name }}</div>
        <div class="kartica-adresa muted">{{ r.address }}</div>
        <div class="kartica-akcija">Pogledaj jelovnik →</div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

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

.lista-restorana {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.kartica-restorana {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.75rem;
  background: white;
  border: 1px solid var(--boja-rub);
  border-radius: 12px;
  transition: all var(--tranzicija);
  box-shadow: var(--sjena);
  cursor: pointer;
}

.kartica-restorana:hover {
  border-color: var(--boja-akcent);
  box-shadow: var(--sjena-lg);
  transform: translateY(-4px);
}

.kartica-naziv {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--boja-tekst);
}

.kartica-adresa {
  font-size: 0.9rem;
  color: var(--boja-tekst-mute);
}

.kartica-akcija {
  font-size: 0.9rem;
  color: var(--boja-akcent);
  margin-top: 0.5rem;
  font-weight: 600;
}
</style>
