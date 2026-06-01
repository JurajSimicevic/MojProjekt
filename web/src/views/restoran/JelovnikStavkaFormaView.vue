<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { kreirajStavku } from '@/services/jelovnik'
import { dohvatiRestorante } from '@/services/restorani'
import Gumb from '@/components/Gumb.vue'
import FormaPolje from '@/components/FormaPolje.vue'
import { ApiGreska } from '@/services/api'

const router = useRouter()
const auth = useAuthStore()
const obavijesti = useObavijestiStore()

const restaurantId = ref<number | null>(null)
const sprema = ref(false)

const forma = ref({ name: '', description: '', price: '', is_available: true })
const greskeForme = ref({ name: '', price: '' })

onMounted(async () => {
  try {
    const sviRestorani = await dohvatiRestorante()
    const mojRestoran = sviRestorani.find((r) => r.owner_id === auth.user?.id)
    if (mojRestoran) restaurantId.value = mojRestoran.id
  } catch {
    obavijesti.greska('Nije moguće dohvatiti restoran.')
  }
})

function validiraj(): boolean {
  greskeForme.value = { name: '', price: '' }
  let ok = true
  if (!forma.value.name.trim()) { greskeForme.value.name = 'Naziv je obavezan.'; ok = false }
  if (!forma.value.price || isNaN(Number(forma.value.price)) || Number(forma.value.price) <= 0) {
    greskeForme.value.price = 'Cijena mora biti pozitivan broj.'
    ok = false
  }
  return ok
}

async function spremi(): Promise<void> {
  if (!validiraj() || !restaurantId.value) return
  sprema.value = true
  try {
    await kreirajStavku({
      name: forma.value.name.trim(),
      description: forma.value.description.trim() || undefined,
      price: Number(forma.value.price),
      is_available: forma.value.is_available,
      restaurant_id: restaurantId.value,
    })
    obavijesti.uspjeh('Stavka dodana na jelovnik.')
    await router.push('/restoran/jelovnik')
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.message : 'Greška pri spremanju.')
  } finally {
    sprema.value = false
  }
}
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Nova stavka</h1>
      <RouterLink to="/restoran/jelovnik" class="akcija">← Natrag</RouterLink>
    </div>

    <div v-if="!restaurantId" class="stanje-poruka greska">
      Nije pronađen restoran za vaš račun.
    </div>

    <form v-else class="forma" @submit.prevent="spremi">
      <FormaPolje
        oznaka="Naziv"
        v-model="forma.name"
        :greska="greskeForme.name"
        obavezno
      />
      <FormaPolje
        oznaka="Opis (opcionalno)"
        v-model="forma.description"
      />
      <FormaPolje
        oznaka="Cijena (€)"
        v-model="forma.price"
        vrsta="number"
        :greska="greskeForme.price"
        obavezno
      />

      <label class="polje-dostupnost">
        <input type="checkbox" v-model="forma.is_available" />
        Odmah dostupno
      </label>

      <div class="forma-akcije">
        <RouterLink to="/restoran/jelovnik">
          <Gumb vrsta="sekundarni">Odustani</Gumb>
        </RouterLink>
        <Gumb tip="submit" :ucitava="sprema">Dodaj stavku</Gumb>
      </div>
    </form>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 1.5rem; max-width: 480px; }

.zaglavlje {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.akcija {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
}

.akcija:hover { color: var(--boja-tekst); }

.forma {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1.5rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
}

.polje-dostupnost {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.forma-akcije {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding-top: 0.5rem;
}

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.stanje-poruka.greska { border-color: var(--boja-opasnost); color: var(--boja-opasnost); }
</style>
