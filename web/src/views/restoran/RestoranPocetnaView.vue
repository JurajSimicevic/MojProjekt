<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { dohvatiRestorante } from '@/services/restorani'
import type { Restoran } from '@/types/restoran'

const auth = useAuthStore()
const mojRestoran = ref<Restoran | null>(null)

onMounted(async () => {
  try {
    const svi = await dohvatiRestorante()
    mojRestoran.value = svi.find((r) => r.owner_id === auth.user?.id) ?? null
  } catch {
    // nije kritično za prikaz
  }
})
</script>

<template>
  <div class="pogled">
    <h1>Restoran — Početna</h1>
    <p class="muted">Dobrodošli, {{ auth.user?.username }}.</p>

    <div v-if="mojRestoran" class="info-restoran">
      <h2>{{ mojRestoran.name }}</h2>
      <p class="muted">{{ mojRestoran.address }}</p>
    </div>

    <div class="kartice">
      <RouterLink to="/restoran/jelovnik" class="kartica">
        <div class="kartica-naslov">Jelovnik</div>
        <div class="kartica-opis muted">Upravljaj stavkama jelovnika</div>
      </RouterLink>
      <RouterLink to="/restoran/narudzbe" class="kartica">
        <div class="kartica-naslov">Narudžbe</div>
        <div class="kartica-opis muted">Pregled i obrada narudžbi</div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }

.info-restoran {
  padding: 1rem 1.5rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  border-left: 3px solid var(--boja-akcent);
}

.kartice {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.kartica {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1.5rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  transition: border-color var(--tranzicija);
}

.kartica:hover { border-color: var(--boja-akcent); }

.kartica-naslov {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kartica-opis { font-size: 0.8rem; }
</style>
