<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { ApiGreska } from '@/services/api'

const router = useRouter()
const auth = useAuthStore()
const obavijesti = useObavijestiStore()

const korisnickoIme = ref('')
const lozinka = ref('')
const ucitava = ref(false)

async function prijava(): Promise<void> {
  if (!korisnickoIme.value || !lozinka.value) return
  ucitava.value = true
  try {
    await auth.login(korisnickoIme.value, lozinka.value)
    if (auth.isAdmin) await router.push('/admin/pocetna')
    else if (auth.isRestoran) await router.push('/restoran/pocetna')
    else if (auth.isDostavljac) await router.push('/dostavljac/pocetna')
    else await router.push('/kupac/pocetna')
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.message : 'Greška pri prijavi.')
  } finally {
    ucitava.value = false
  }
}
</script>

<template>
  <div class="prijava-kontejner">
    <div class="prijava">
      <div class="zaglavlje">
        <h1>🚀 Dostava Hrane</h1>
        <p class="podnaslov">Sve što trebaš je jedno kliknutse</p>
      </div>

      <form class="forma" @submit.prevent="prijava">
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
            autocomplete="current-password"
            required
          />
        </div>
        <button type="submit" class="gumb-prijava" :disabled="ucitava">
          {{ ucitava ? 'Učitavanje...' : 'Prijavi se' }}
        </button>
      </form>

      <div class="podaci">
        <p>Test korisnici:</p>
        <ul>
          <li><strong>Kupac:</strong> customer1 / cust123</li>
          <li><strong>Kurir:</strong> courier1 / cour123</li>
          <li><strong>Admin:</strong> admin / admin123</li>
        </ul>
      </div>

      <p class="registracija-link">
        Nemaš račun?
        <RouterLink to="/registracija" class="link">Registriraj se</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.prijava-kontejner {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #00c853 0%, #00a840 100%);
  padding: 2rem;
}

.prijava {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.zaglavlje { margin-bottom: 2rem; text-align: center; }

h1 {
  font-size: 2.25rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--boja-tekst);
}

.podnaslov {
  color: var(--boja-tekst-mute);
  font-size: 1rem;
}

.forma {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.polje {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

label {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--boja-tekst);
}

input {
  background: var(--boja-povrsina);
  border: 1.5px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  transition: all var(--tranzicija);
}

input:focus {
  outline: none;
  border-color: var(--boja-akcent);
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.1);
}

input::placeholder {
  color: var(--boja-tekst-mute);
}

.gumb-prijava {
  background: var(--boja-akcent);
  color: white;
  font-weight: 700;
  font-size: 1.05rem;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--tranzicija);
  margin-top: 0.5rem;
}

.gumb-prijava:hover:not(:disabled) {
  background: var(--boja-akcent-tamno);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 200, 83, 0.3);
}

.gumb-prijava:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.podaci {
  background: var(--boja-povrsina);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: var(--boja-tekst-mute);
}

.podaci p {
  font-weight: 600;
  color: var(--boja-tekst);
  margin-bottom: 0.5rem;
}

.podaci ul {
  list-style: none;
  padding-left: 0;
}

.podaci li {
  padding: 0.35rem 0;
  font-size: 0.85rem;
}

.registracija-link {
  font-size: 0.95rem;
  color: var(--boja-tekst-mute);
  text-align: center;
}

.link {
  color: var(--boja-akcent);
  font-weight: 600;
  transition: color var(--tranzicija);
}

.link:hover {
  color: var(--boja-akcent-tamno);
}
.link:hover { text-decoration: underline; }
</style>
