<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiMojeNarudzbe, promijeniStatus } from '@/services/narudzbe'
import StatusBadge from '@/components/StatusBadge.vue'
import Gumb from '@/components/Gumb.vue'
import type { Narudzba, StatusNarudzbe } from '@/types/narudzba'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const obavijesti = useObavijestiStore()
const narudzbe = ref<Narudzba[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

const sljedeciStatus: Partial<Record<StatusNarudzbe, StatusNarudzbe>> = {
  pending: 'accepted',
  accepted: 'preparing',
  preparing: 'ready',
}

const oznakaAkcije: Partial<Record<StatusNarudzbe, string>> = {
  pending: 'Prihvati',
  accepted: 'Priprema',
  preparing: 'Spremi',
}

async function ucitaj(): Promise<void> {
  stanje.value = 'ucitavanje'
  try {
    const podaci = await dohvatiMojeNarudzbe()
    narudzbe.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška.'
  }
}

async function napredujStatus(narudzba: Narudzba): Promise<void> {
  const novi = sljedeciStatus[narudzba.status]
  if (!novi) return
  try {
    await promijeniStatus(narudzba.id, novi)
    obavijesti.uspjeh(`Status ažuriran: ${novi}`)
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
      <h1>Narudžbe restorana</h1>
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
        <div class="kartica-stavke">
          <span v-for="s in n.items" :key="s.id" class="stavka">
            {{ s.item_name }} — {{ s.price_at_purchase.toFixed(2) }} €
          </span>
        </div>
        <div class="kartica-footer">
          <span><strong>Ukupno: {{ n.total_price.toFixed(2) }} €</strong></span>
          <Gumb
            v-if="sljedeciStatus[n.status]"
            velicina="mali"
            @click="napredujStatus(n)"
          >
            {{ oznakaAkcije[n.status] ?? 'Napreduj' }}
          </Gumb>
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

.lista-narudzbi { display: flex; flex-direction: column; gap: 0.75rem; }

.kartica-narudzbe {
  padding: 1rem 1.25rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.kartica-zaglavlje { display: flex; align-items: center; gap: 0.75rem; }

.kartica-id {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
}

.kartica-stavke { display: flex; flex-direction: column; gap: 0.25rem; }

.stavka { font-size: 0.85rem; color: var(--boja-tekst-mute); }

.kartica-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.875rem;
}
</style>
