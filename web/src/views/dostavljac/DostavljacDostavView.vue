<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiMojeNarudzbe, promijeniStatus } from '@/services/narudzbe'
import StatusBadge from '@/components/StatusBadge.vue'
import Gumb from '@/components/Gumb.vue'
import type { Narudzba } from '@/types/narudzba'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const obavijesti = useObavijestiStore()
const narudzbe = ref<Narudzba[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

const dostupne = computed(() => narudzbe.value.filter((n) => n.status === 'ready'))
const aktivne = computed(() => narudzbe.value.filter((n) => n.status === 'on_the_way'))

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

async function preuzmiiNarudzbu(id: number): Promise<void> {
  try {
    await promijeniStatus(id, 'on_the_way')
    obavijesti.uspjeh('Narudžba preuzeta! Na putu...')
    await ucitaj()
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška.')
  }
}

async function isporuciNarudzbu(id: number): Promise<void> {
  try {
    await promijeniStatus(id, 'delivered')
    obavijesti.uspjeh('Narudžba isporučena!')
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
      <h1>Dostave</h1>
      <Gumb vrsta="sekundarni" velicina="mali" @click="ucitaj">Osvježi</Gumb>
    </div>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">{{ porukaGreske }}</div>
    <div v-else>
      <section class="sekcija">
        <h2>Dostupno za preuzimanje</h2>
        <div v-if="dostupne.length === 0" class="stanje-poruka muted">
          Nema narudžbi čekaju preuzimanje.
        </div>
        <div v-else class="lista-narudzbi">
          <div v-for="n in dostupne" :key="n.id" class="kartica-narudzbe kartica--dostupna">
            <div class="kartica-zaglavlje">
              <span class="kartica-id">#{{ n.id }}</span>
              <StatusBadge :status="n.status" />
            </div>
            <div class="kartica-stavke">
              <span v-for="s in n.items" :key="s.id" class="stavka">
                {{ s.item_name }}
              </span>
            </div>
            <div class="kartica-footer">
              <span class="muted">Restoran: {{ n.restaurant_id }}</span>
              <Gumb velicina="mali" @click="preuzmiiNarudzbu(n.id)">Preuzmi</Gumb>
            </div>
          </div>
        </div>
      </section>

      <section class="sekcija">
        <h2>Moje aktivne dostave</h2>
        <div v-if="aktivne.length === 0" class="stanje-poruka muted">
          Nema aktivnih dostava.
        </div>
        <div v-else class="lista-narudzbi">
          <div v-for="n in aktivne" :key="n.id" class="kartica-narudzbe kartica--aktivna">
            <div class="kartica-zaglavlje">
              <span class="kartica-id">#{{ n.id }}</span>
              <StatusBadge :status="n.status" />
            </div>
            <div class="kartica-stavke">
              <span v-for="s in n.items" :key="s.id" class="stavka">
                {{ s.item_name }}
              </span>
            </div>
            <div class="kartica-footer">
              <span><strong>{{ n.total_price.toFixed(2) }} €</strong></span>
              <Gumb velicina="mali" @click="isporuciNarudzbu(n.id)">Isporučeno</Gumb>
            </div>
          </div>
        </div>
      </section>
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

.sekcija { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem; }

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

.kartica--dostupna { border-left: 3px solid var(--boja-uspjeh); }
.kartica--aktivna  { border-left: 3px solid var(--boja-akcent); }

.kartica-zaglavlje { display: flex; align-items: center; gap: 0.75rem; }

.kartica-id {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
}

.kartica-stavke { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.stavka { font-size: 0.8rem; color: var(--boja-tekst-mute); }

.kartica-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.875rem;
}
</style>
