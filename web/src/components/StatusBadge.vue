<script setup lang="ts">
defineProps<{ status: string }>()
</script>

<template>
  <span :class="['badge', `badge--${status}`]">{{ status }}</span>
</template>

<style scoped>
.badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  white-space: nowrap;
  display: inline-block;
  border: none;
}

.badge--pending {
  color: var(--boja-tekst-mute);
  background: #f0f0f0;
}

.badge--accepted {
  color: white;
  background: var(--boja-akcent);
}

.badge--preparing {
  color: white;
  background: var(--boja-akcent);
}

.badge--ready {
  color: white;
  background: var(--boja-uspjeh);
}

.badge--on_the_way {
  color: white;
  background: var(--boja-akcent);
}

.badge--delivered {
  color: white;
  background: var(--boja-uspjeh);
}

.badge--cancelled {
  color: white;
  background: var(--boja-opasnost);
}
</style>
