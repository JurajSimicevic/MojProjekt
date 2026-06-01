<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiRestorante, kreirajRestoran } from '@/services/restorani'
import Tablica from '@/components/Tablica.vue'
import Gumb from '@/components/Gumb.vue'
import Modal from '@/components/Modal.vue'
import FormaPolje from '@/components/FormaPolje.vue'
import type { Restoran } from '@/types/restoran'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const obavijesti = useObavijestiStore()
const restorani = ref<Restoran[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')
const pokaziModal = ref(false)
const sprema = ref(false)

const forma = ref({ name: '', address: '', owner_id: '' })
const greskeForme = ref({ name: '', address: '', owner_id: '' })

const stupci = [
  { kljuc: 'id', oznaka: 'ID' },
  { kljuc: 'name', oznaka: 'Naziv' },
  { kljuc: 'address', oznaka: 'Adresa' },
  { kljuc: 'owner_id', oznaka: 'Vlasnik ID' },
]

async function ucitaj(): Promise<void> {
  stanje.value = 'ucitavanje'
  try {
    const podaci = await dohvatiRestorante()
    restorani.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
  }
}

function validiraj(): boolean {
  greskeForme.value = { name: '', address: '', owner_id: '' }
  let ok = true
  if (!forma.value.name.trim()) { greskeForme.value.name = 'Naziv je obavezan.'; ok = false }
  if (!forma.value.address.trim()) { greskeForme.value.address = 'Adresa je obavezna.'; ok = false }
  if (!forma.value.owner_id || isNaN(Number(forma.value.owner_id))) {
    greskeForme.value.owner_id = 'Unesi valjani ID vlasnika.'
    ok = false
  }
  return ok
}

async function kreiraj(): Promise<void> {
  if (!validiraj()) return
  sprema.value = true
  try {
    await kreirajRestoran({
      name: forma.value.name.trim(),
      address: forma.value.address.trim(),
      owner_id: Number(forma.value.owner_id),
    })
    obavijesti.uspjeh('Restoran kreiran.')
    pokaziModal.value = false
    forma.value = { name: '', address: '', owner_id: '' }
    await ucitaj()
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri kreiranju.')
  } finally {
    sprema.value = false
  }
}

onMounted(ucitaj)
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Restorani</h1>
      <Gumb @click="pokaziModal = true">+ Novi restoran</Gumb>
    </div>

    <Tablica
      :stupci="stupci"
      :redovi="(restorani as Record<string, unknown>[])"
      :stanje="stanje"
      :poruka-prazno="'Nema restorana. Dodajte prvi restoran.'"
      :poruka-greske="porukaGreske"
    />

    <Modal v-model="pokaziModal" naslov="Novi restoran">
      <FormaPolje
        oznaka="Naziv"
        v-model="forma.name"
        :greska="greskeForme.name"
        obavezno
      />
      <FormaPolje
        oznaka="Adresa"
        v-model="forma.address"
        :greska="greskeForme.address"
        obavezno
      />
      <FormaPolje
        oznaka="ID vlasnika (restaurant korisnik)"
        v-model="forma.owner_id"
        vrsta="number"
        :greska="greskeForme.owner_id"
        pomoc="Najprije kreirajte restaurant korisnika u Osoblje."
        obavezno
      />
      <template #akcije>
        <Gumb vrsta="sekundarni" @click="pokaziModal = false">Odustani</Gumb>
        <Gumb :ucitava="sprema" @click="kreiraj">Spremi</Gumb>
      </template>
    </Modal>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 1.5rem; }

.zaglavlje {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
</style>
