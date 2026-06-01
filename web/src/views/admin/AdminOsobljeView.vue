<script setup lang="ts">
import { ref } from 'vue'
import { useObavijestiStore } from '@/stores/obavijesti'
import { kreirajOsoblje } from '@/services/korisnici'
import Gumb from '@/components/Gumb.vue'
import FormaPolje from '@/components/FormaPolje.vue'
import type { KorisnikPodaci } from '@/types/korisnik'
import { ApiGreska } from '@/services/api'

const obavijesti = useObavijestiStore()
const sprema = ref(false)
const noviKorisnik = ref<KorisnikPodaci | null>(null)

const forma = ref({ username: '', password: '', role: 'restaurant' as 'restaurant' | 'courier' })
const greskeForme = ref({ username: '', password: '' })

function validiraj(): boolean {
  greskeForme.value = { username: '', password: '' }
  let ok = true
  if (!forma.value.username.trim()) { greskeForme.value.username = 'Korisničko ime je obavezno.'; ok = false }
  if (!forma.value.password) { greskeForme.value.password = 'Lozinka je obavezna.'; ok = false }
  return ok
}

async function kreiraj(): Promise<void> {
  if (!validiraj()) return
  sprema.value = true
  noviKorisnik.value = null
  try {
    const korisnik = await kreirajOsoblje({
      username: forma.value.username.trim(),
      password: forma.value.password,
      role: forma.value.role,
    })
    noviKorisnik.value = korisnik
    obavijesti.uspjeh(`Korisnik "${korisnik.username}" kreiran (ID: ${korisnik.id}).`)
    forma.value = { username: '', password: '', role: 'restaurant' }
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.message : 'Greška pri kreiranju.')
  } finally {
    sprema.value = false
  }
}
</script>

<template>
  <div class="pogled">
    <h1>Osoblje</h1>
    <p class="muted">Kreiraj korisničke račune za restorane i dostavljače.</p>

    <div class="kartica">
      <h2>Novi zaposlenik</h2>

      <div class="forma">
        <FormaPolje
          oznaka="Korisničko ime"
          v-model="forma.username"
          :greska="greskeForme.username"
          obavezno
        />
        <FormaPolje
          oznaka="Lozinka"
          v-model="forma.password"
          vrsta="password"
          :greska="greskeForme.password"
          obavezno
        />

        <div class="polje-uloga">
          <label class="oznaka-uloge">Uloga</label>
          <div class="opcije-uloge">
            <label class="opcija">
              <input type="radio" v-model="forma.role" value="restaurant" />
              Restaurant
            </label>
            <label class="opcija">
              <input type="radio" v-model="forma.role" value="courier" />
              Courier
            </label>
          </div>
        </div>

        <Gumb :ucitava="sprema" @click="kreiraj">Kreiraj korisnika</Gumb>
      </div>
    </div>

    <div v-if="noviKorisnik" class="rezultat">
      <p class="uspjeh">Korisnik kreiran:</p>
      <p><strong>ID:</strong> {{ noviKorisnik.id }}</p>
      <p><strong>Korisničko ime:</strong> {{ noviKorisnik.username }}</p>
      <p><strong>Uloga:</strong> {{ noviKorisnik.role }}</p>
      <p class="muted" v-if="noviKorisnik.role === 'restaurant'">
        Koristite ovaj ID ({{ noviKorisnik.id }}) pri kreiranju restorana kao "ID vlasnika".
      </p>
    </div>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }

.kartica {
  padding: 1.5rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-width: 480px;
}

.forma { display: flex; flex-direction: column; gap: 1rem; }

.polje-uloga { display: flex; flex-direction: column; gap: 0.4rem; }

.oznaka-uloge {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
}

.opcije-uloge { display: flex; gap: 1.5rem; }

.opcija {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.rezultat {
  padding: 1rem 1.5rem;
  border: 1px solid var(--boja-uspjeh);
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  max-width: 480px;
  font-size: 0.875rem;
}

.uspjeh { color: var(--boja-uspjeh); font-weight: 500; }
</style>
