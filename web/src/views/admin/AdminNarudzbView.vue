<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dohvatiMojeNarudzbe, promijeniStatus } from '@/services/narudzbe'
import { useObavijestiStore } from '@/stores/obavijesti'
import StatusBadge from '@/components/StatusBadge.vue'
import Gumb from '@/components/Gumb.vue'
import type { Narudzba } from '@/types/narudzba'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const obavijesti = useObavijestiStore()
const narudzbe = ref<Narudzba[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

async function ucitaj(): Promise<void> {
  stanje.value = 'ucitavanje'
  try {
    const podaci = await dohvatiMojeNarudzbe()
    narudzbe.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
  }
}

async function otkaziNarudzbu(id: number): Promise<void> {
  if (!confirm('Otkazati narudžbu?')) return
  try {
    await promijeniStatus(id, 'cancelled')
    obavijesti.uspjeh('Narudžba otkazana.')
    await ucitaj()
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška.')
  }
}

onMounted(ucitaj)
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Sve narudžbe</h1>
      <Gumb vrsta="sekundarni" velicina="mali" @click="ucitaj">Osvježi</Gumb>
    </div>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">{{ porukaGreske }}</div>
    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">Nema narudžbi.</div>
    <div v-else class="lista-narudzbi">
      <div v-for="n in narudzbe" :key="n.id" class="kartica-narudzbe">
        <div class="kartica-zaglavlje">
          <span class="kartica-id">#{{ n.id }}</span>
          <StatusBadge :status="n.status" />
        </div>
        <div class="kartica-info">
          <span class="muted">Kupac: {{ n.customer_id }}</span>
          <span class="muted">Restoran: {{ n.restaurant_id }}</span>
          <span>Ukupno: <strong>{{ n.total_price.toFixed(2) }} €</strong></span>
        </div>
        <div class="kartica-akcije">
          <Gumb
            v-if="n.status === 'pending'"
            vrsta="opasnost"
            velicina="mali"
            @click="otkaziNarudzbu(n.id)"
          >Otkaži</Gumb>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 1.5rem; }

.zaglavlje {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.stanje-poruka.greska { border-color: var(--boja-opasnost); color: var(--boja-opasnost); }

.lista-narudzbi {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.kartica-narudzbe {
  padding: 1rem 1.25rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.kartica-zaglavlje {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 120px;
}

.kartica-id {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
}

.kartica-info {
  display: flex;
  gap: 1.5rem;
  flex: 1;
  font-size: 0.875rem;
  flex-wrap: wrap;
}

.kartica-akcije { margin-left: auto; }
</style>
