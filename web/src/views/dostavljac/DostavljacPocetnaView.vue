<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <div class="pogled">
    <h1>Dostavljač — Početna</h1>
    <p class="muted">Dobrodošli, {{ auth.user?.username }}.</p>

    <div class="kartice">
      <RouterLink to="/dostavljac/dostave" class="kartica">
        <div class="kartica-naslov">Dostave</div>
        <div class="kartica-opis muted">Preuzmi i isporuči narudžbe</div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }

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
}

.kartica-opis { font-size: 0.8rem; }
</style>
