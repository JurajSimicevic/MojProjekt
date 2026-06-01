<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiJelovnik, promijeniDostupnost } from '@/services/jelovnik'
import { dohvatiRestorante } from '@/services/restorani'
import Gumb from '@/components/Gumb.vue'
import type { StavkaJelovnika } from '@/types/stavka_jelovnika'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const auth = useAuthStore()
const obavijesti = useObavijestiStore()
const stavke = ref<StavkaJelovnika[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')
const restaurantId = ref<number | null>(null)

const stupci = [
  { kljuc: 'name', oznaka: 'Naziv' },
  { kljuc: 'description', oznaka: 'Opis' },
  { kljuc: 'price', oznaka: 'Cijena (€)' },
  { kljuc: 'is_available', oznaka: 'Dostupno' },
]

async function ucitaj(): Promise<void> {
  stanje.value = 'ucitavanje'
  try {
    const sviRestorani = await dohvatiRestorante()
    const mojRestoran = sviRestorani.find((r) => r.owner_id === auth.user?.id)
    if (!mojRestoran) {
      stanje.value = 'prazno'
      porukaGreske.value = 'Nema restorana povezanog s vašim računom.'
      return
    }
    restaurantId.value = mojRestoran.id
    const podaci = await dohvatiJelovnik(mojRestoran.id)
    stavke.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
  }
}

async function promijeniDostupnostStavke(id: number, trenutno: boolean): Promise<void> {
  try {
    await promijeniDostupnost(id, !trenutno)
    obavijesti.uspjeh('Dostupnost ažurirana.')
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
      <h1>Jelovnik</h1>
      <RouterLink v-if="restaurantId" to="/restoran/jelovnik/nova-stavka">
        <Gumb>+ Nova stavka</Gumb>
      </RouterLink>
    </div>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">{{ porukaGreske }}</div>
    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">
      Nema stavki na jelovniku. Dodajte prvu stavku.
    </div>
    <table v-else class="tablica">
      <thead>
        <tr>
          <th v-for="s in stupci" :key="s.kljuc">{{ s.oznaka }}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stavka in stavke" :key="stavka.id">
          <td>{{ stavka.name }}</td>
          <td class="muted">{{ stavka.description ?? '—' }}</td>
          <td>{{ stavka.price.toFixed(2) }}</td>
          <td>
            <span :class="stavka.is_available ? 'dostupno' : 'nedostupno'">
              {{ stavka.is_available ? 'Da' : 'Ne' }}
            </span>
          </td>
          <td class="akcije">
            <Gumb
              :vrsta="stavka.is_available ? 'sekundarni' : 'primarni'"
              velicina="mali"
              @click="promijeniDostupnostStavke(stavka.id, stavka.is_available)"
            >
              {{ stavka.is_available ? 'Deaktiviraj' : 'Aktiviraj' }}
            </Gumb>
          </td>
        </tr>
      </tbody>
    </table>
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

.tablica { width: 100%; border-collapse: collapse; font-size: 0.875rem; }

.tablica th {
  text-align: left;
  padding: 0.625rem 1rem;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
  border-bottom: 2px solid var(--boja-rub);
}

.tablica td { padding: 0.75rem 1rem; border-bottom: 1px solid var(--boja-rub); }
.tablica tbody tr:hover td { background: var(--boja-povrsina); }
.akcije { display: flex; gap: 0.5rem; }

.dostupno { color: var(--boja-uspjeh); }
.nedostupno { color: var(--boja-tekst-mute); }
</style>
