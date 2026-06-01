<script setup lang="ts">
</script>

<template>
  <div class="nepoznato">
    <h1>404</h1>
    <p class="muted">Stranica nije pronađena.</p>
    <RouterLink to="/" class="link">← Početna</RouterLink>
  </div>
</template>

<style scoped>
.nepoznato {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

h1 {
  font-family: var(--font-display);
  font-size: 6rem;
  color: var(--boja-akcent);
}

.link {
  font-size: 0.85rem;
  color: var(--boja-tekst-mute);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.link:hover { color: var(--boja-tekst); }
</style>
