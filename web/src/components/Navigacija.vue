<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

async function odjava(): Promise<void> {
  auth.logout()
  await router.push('/prijava')
}
</script>

<template>
  <nav class="nav">
    <RouterLink to="/" class="brand">BRZA DOSTAVA</RouterLink>

    <div v-if="auth.isAdmin" class="linkovi">
      <RouterLink to="/admin/pocetna" class="link">Početna</RouterLink>
      <RouterLink to="/admin/restorani" class="link">Restorani</RouterLink>
      <RouterLink to="/admin/osoblje" class="link">Osoblje</RouterLink>
      <RouterLink to="/admin/narudzbe" class="link">Narudžbe</RouterLink>
    </div>

    <div v-else-if="auth.isRestoran" class="linkovi">
      <RouterLink to="/restoran/pocetna" class="link">Početna</RouterLink>
      <RouterLink to="/restoran/jelovnik" class="link">Jelovnik</RouterLink>
      <RouterLink to="/restoran/narudzbe" class="link">Narudžbe</RouterLink>
    </div>

    <div v-else-if="auth.isDostavljac" class="linkovi">
      <RouterLink to="/dostavljac/pocetna" class="link">Početna</RouterLink>
      <RouterLink to="/dostavljac/dostave" class="link">Dostave</RouterLink>
    </div>

    <div v-else-if="auth.isKupac" class="linkovi">
      <RouterLink to="/kupac/pocetna" class="link">Početna</RouterLink>
      <RouterLink to="/kupac/restorani" class="link">Restorani</RouterLink>
      <RouterLink to="/kupac/narudzbe" class="link">Narudžbe</RouterLink>
    </div>

    <div v-if="auth.isAuthenticated" class="desno">
      <span class="korisnik">{{ auth.user?.username }}</span>
      <button class="gumb-odjava" @click="odjava">Odjava</button>
    </div>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 0 1.5rem;
  height: 64px;
  background: white;
  border-bottom: 1px solid var(--boja-rub);
  box-shadow: var(--sjena);
}

.brand {
  font-weight: 700;
  font-size: 1.4rem;
  color: var(--boja-akcent);
  white-space: nowrap;
  letter-spacing: 0;
}

.linkovi {
  display: flex;
  align-items: center;
  gap: 0;
  flex: 1;
}

.link {
  font-size: 0.95rem;
  color: var(--boja-tekst-mute);
  padding: 0.5rem 1rem;
  transition: all var(--tranzicija);
  font-weight: 500;
  border-bottom: 2px solid transparent;
}

.link:hover {
  color: var(--boja-tekst);
  background: var(--boja-povrsina);
  border-radius: 6px;
}

.link.router-link-active {
  color: var(--boja-akcent);
  border-bottom-color: var(--boja-akcent);
  background: transparent;
}

.desno {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.korisnik {
  font-size: 0.95rem;
  color: var(--boja-tekst);
  font-weight: 500;
}

.gumb-odjava {
  background: transparent;
  color: var(--boja-tekst-mute);
  border: 1px solid var(--boja-rub);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--tranzicija);
}

.gumb-odjava:hover {
  color: var(--boja-opasnost);
  border-color: var(--boja-opasnost);
  background: var(--boja-povrsina);
}


.korisnik {
  font-size: 0.75rem;
  color: var(--boja-tekst-mute);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.gumb-odjava {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--boja-rub);
  transition: color var(--tranzicija), border-color var(--tranzicija);
}

.gumb-odjava:hover {
  color: var(--boja-akcent);
  border-color: var(--boja-akcent);
}
</style>
