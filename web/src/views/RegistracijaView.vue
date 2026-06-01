<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useObavijestiStore } from '@/stores/obavijesti'
import { registrirajKupca } from '@/services/korisnici'
import { ApiGreska } from '@/services/api'

const router = useRouter()
const obavijesti = useObavijestiStore()

const korisnickoIme = ref('')
const lozinka = ref('')
const lozinkaPotvrda = ref('')
const ucitava = ref(false)
const greska = ref('')

async function registracija(): Promise<void> {
  greska.value = ''
  if (lozinka.value !== lozinkaPotvrda.value) {
    greska.value = 'Lozinke se ne podudaraju.'
    return
  }
  if (lozinka.value.length < 1) {
    greska.value = 'Lozinka je obavezna.'
    return
  }
  ucitava.value = true
  try {
    await registrirajKupca({ username: korisnickoIme.value, password: lozinka.value })
    obavijesti.uspjeh('Registracija uspješna! Prijavite se.')
    await router.push('/prijava')
  } catch (e) {
    greska.value = e instanceof ApiGreska ? e.message : 'Greška pri registraciji.'
  } finally {
    ucitava.value = false
  }
}
</script>

<template>
  <div class="registracija">
    <h1>REGISTRACIJA</h1>
    <p class="podnaslov">Naručuj hranu iz omiljenih restorana</p>

    <form class="forma" @submit.prevent="registracija">
      <div class="polje">
        <label for="korisnicko-ime">Korisničko ime</label>
        <input
          id="korisnicko-ime"
          v-model="korisnickoIme"
          type="text"
          placeholder="korisnik"
          autocomplete="username"
          required
        />
      </div>
      <div class="polje">
        <label for="lozinka">Lozinka</label>
        <input
          id="lozinka"
          v-model="lozinka"
          type="password"
          placeholder="••••••••"
          autocomplete="new-password"
          required
        />
      </div>
      <div class="polje">
        <label for="lozinka-potvrda">Potvrdi lozinku</label>
        <input
          id="lozinka-potvrda"
          v-model="lozinkaPotvrda"
          type="password"
          placeholder="••••••••"
          autocomplete="new-password"
          required
        />
      </div>
      <p v-if="greska" class="greska-poruka">{{ greska }}</p>
      <button type="submit" class="gumb-registracija" :disabled="ucitava">
        {{ ucitava ? 'REGISTRACIJA...' : 'REGISTRIRAJ SE' }}
      </button>
    </form>

    <p class="prijava-link">
      Već imaš račun?
      <RouterLink to="/prijava" class="link">Prijavi se</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.registracija {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

h1 {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 3rem;
  letter-spacing: 0.08em;
  color: var(--boja-akcent);
}

.podnaslov {
  color: var(--boja-tekst-mute);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: -1.5rem;
}

.forma {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 2rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
}

.polje { display: flex; flex-direction: column; gap: 0.5rem; }

label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--boja-tekst-mute);
}

input {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.75rem 1rem;
  transition: border-color var(--tranzicija);
}

input:focus { outline: none; border-color: var(--boja-akcent); }
input::placeholder { color: var(--boja-tekst-mute); opacity: 0.6; }

.greska-poruka {
  font-size: 0.8rem;
  color: var(--boja-opasnost);
  padding: 0.5rem;
  border: 1px solid var(--boja-opasnost);
}

.gumb-registracija {
  background: var(--boja-akcent);
  color: var(--boja-pozadina);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 0.875rem;
  margin-top: 0.5rem;
  cursor: pointer;
  border: none;
}

.gumb-registracija:hover:not(:disabled) { background: var(--boja-tekst); color: var(--boja-pozadina); }
.gumb-registracija:disabled { opacity: 0.5; cursor: not-allowed; }

.prijava-link {
  font-size: 0.8rem;
  color: var(--boja-tekst-mute);
  text-align: center;
}

.link { color: var(--boja-akcent); }
.link:hover { text-decoration: underline; }
</style>
