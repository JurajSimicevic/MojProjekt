<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <div class="pogled">
    <h1>Dobrodošli!</h1>
    <p class="muted">Naručite hradu iz omiljenog restorana, {{ auth.user?.username }}.</p>

    <div class="kartice">
      <RouterLink to="/kupac/restorani" class="kartica">
        <div class="kartica-naslov">Restorani</div>
        <div class="kartica-opis muted">Pregledaj ponudu i naruči</div>
      </RouterLink>
      <RouterLink to="/kupac/narudzbe" class="kartica">
        <div class="kartica-naslov">Narudžbe</div>
        <div class="kartica-opis muted">Prati status svojih narudžbi</div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: var(--boja-tekst);
}

p.muted {
  font-size: 1.05rem;
  color: var(--boja-tekst-mute);
}

.kartice {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.kartica {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 2rem;
  background: white;
  border: 1px solid var(--boja-rub);
  border-radius: 12px;
  transition: all var(--tranzicija);
  box-shadow: var(--sjena);
  cursor: pointer;
}

.kartica:hover {
  border-color: var(--boja-akcent);
  box-shadow: var(--sjena-lg);
  transform: translateY(-4px);
}

.kartica-naslov {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--boja-tekst);
}

.kartica-opis {
  font-size: 0.95rem;
  color: var(--boja-tekst-mute);
}
</style>
