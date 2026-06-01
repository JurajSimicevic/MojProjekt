<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiRestoran } from '@/services/restorani'
import { dohvatiJelovnik } from '@/services/jelovnik'
import { kreirajNarudzbu } from '@/services/narudzbe'
import Gumb from '@/components/Gumb.vue'
import { ApiGreska } from '@/services/api'
import type { StavkaJelovnika } from '@/types/stavka_jelovnika'
import type { Restoran } from '@/types/restoran'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const route = useRoute()
const router = useRouter()
const obavijesti = useObavijestiStore()

const restaurantId = Number(route.params['id'])
const restoran = ref<Restoran | null>(null)
const stavke = ref<StavkaJelovnika[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')
const odabraneStavke = ref<number[]>([])
const naruci = ref(false)

const ukupno = computed(() => {
  return odabraneStavke.value.reduce((sum, id) => {
    const stavka = stavke.value.find((s) => s.id === id)
    return sum + (stavka?.price ?? 0)
  }, 0)
})

function toggleStavka(id: number): void {
  const idx = odabraneStavke.value.indexOf(id)
  if (idx === -1) odabraneStavke.value.push(id)
  else odabraneStavke.value.splice(idx, 1)
}

async function ucitaj(): Promise<void> {
  stanje.value = 'ucitavanje'
  try {
    const [restoranData, stavkeData] = await Promise.all([
      dohvatiRestoran(restaurantId),
      dohvatiJelovnik(restaurantId),
    ])
    restoran.value = restoranData
    stavke.value = stavkeData.filter((s) => s.is_available)
    stanje.value = stavke.value.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška.'
  }
}

async function posaljiNarudzbu(): Promise<void> {
  if (odabraneStavke.value.length === 0) {
    obavijesti.info('Odaberite barem jednu stavku.')
    return
  }
  naruci.value = true
  try {
    const narudzba = await kreirajNarudzbu({
      restaurant_id: restaurantId,
      item_ids: odabraneStavke.value,
    })
    obavijesti.uspjeh(`Narudžba #${narudzba.id} uspješno poslana!`)
    await router.push('/kupac/narudzbe')
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.message : 'Greška pri slanju narudžbe.')
  } finally {
    naruci.value = false
  }
}

onMounted(ucitaj)
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <div>
        <h1>{{ restoran?.name ?? 'Restoran' }}</h1>
        <p v-if="restoran" class="muted">{{ restoran.address }}</p>
      </div>
      <RouterLink to="/kupac/restorani" class="akcija">← Natrag</RouterLink>
    </div>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">{{ porukaGreske }}</div>
    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">
      Nema dostupnih stavki na jelovniku.
    </div>
    <div v-else class="sadrzaj">
      <div class="jelovnik">
        <h2>Jelovnik</h2>
        <div class="lista-stavki">
          <label
            v-for="s in stavke"
            :key="s.id"
            :class="['stavka', { 'stavka--odabrana': odabraneStavke.includes(s.id) }]"
            @click="toggleStavka(s.id)"
          >
            <div class="stavka-info">
              <div class="stavka-naziv">{{ s.name }}</div>
              <div v-if="s.description" class="stavka-opis muted">{{ s.description }}</div>
            </div>
            <div class="stavka-cijena">{{ s.price.toFixed(2) }} €</div>
            <div class="stavka-checkbox">
              <input
                type="checkbox"
                :checked="odabraneStavke.includes(s.id)"
                @click.stop="toggleStavka(s.id)"
              />
            </div>
          </label>
        </div>
      </div>

      <div class="narucivanje">
        <h2>Narudžba</h2>
        <div v-if="odabraneStavke.length === 0" class="muted" style="font-size: 0.875rem;">
          Odaberite stavke s jelovnika.
        </div>
        <div v-else class="odabrane-stavke">
          <div v-for="id in odabraneStavke" :key="id" class="odabrana-stavka">
            <span>{{ stavke.find((s) => s.id === id)?.name }}</span>
            <span>{{ stavke.find((s) => s.id === id)?.price.toFixed(2) }} €</span>
          </div>
          <div class="ukupno">
            <strong>Ukupno:</strong>
            <strong>{{ ukupno.toFixed(2) }} €</strong>
          </div>
        </div>
        <Gumb
          :onemoguceno="odabraneStavke.length === 0"
          :ucitava="naruci"
          @click="posaljiNarudzbu"
          style="width: 100%; margin-top: 1rem;"
        >
          Naruči
        </Gumb>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 1.5rem; }

.zaglavlje {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.akcija {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
}

.akcija:hover { color: var(--boja-tekst); }

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.stanje-poruka.greska { border-color: var(--boja-opasnost); color: var(--boja-opasnost); }

.sadrzaj {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 768px) {
  .sadrzaj { grid-template-columns: 1fr; }
}

.jelovnik { display: flex; flex-direction: column; gap: 1rem; }

.lista-stavki { display: flex; flex-direction: column; gap: 0.5rem; }

.stavka {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  cursor: pointer;
  transition: border-color var(--tranzicija);
}

.stavka:hover { border-color: var(--boja-akcent); }
.stavka--odabrana { border-color: var(--boja-akcent); background: var(--boja-povrsina); }

.stavka-info { flex: 1; }
.stavka-naziv { font-weight: 500; }
.stavka-opis { font-size: 0.8rem; margin-top: 0.2rem; }

.stavka-cijena {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  white-space: nowrap;
}

.narucivanje {
  position: sticky;
  top: 1rem;
  padding: 1.5rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.odabrane-stavke { display: flex; flex-direction: column; gap: 0.5rem; }

.odabrana-stavka {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.ukupno {
  display: flex;
  justify-content: space-between;
  padding-top: 0.75rem;
  border-top: 1px solid var(--boja-rub);
  font-size: 0.9rem;
}
</style>
