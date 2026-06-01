<script setup lang="ts">
import Navigacija from '@/components/Navigacija.vue'
</script>

<template>
  <div class="layout-aplikacija">
    <Navigacija />
    <main class="sadrzaj">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.layout-aplikacija {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr;
  background: var(--boja-pozadina);
}

.sadrzaj {
  padding: 2rem 1.5rem;
}
</style>
