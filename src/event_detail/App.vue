<!--============================================================ ...
     App tab
... ============================================================ -->

<script setup>
  import "@/assets/app.css"
  import Navigation from "@/components/Navigation.vue"
  import { ref } from 'vue'

  const toggle_states = ref([]);

  function handleToggleUpdate(toggle_states_emitted) {
    toggle_states.value = toggle_states_emitted.value;
  }
  
</script>

<template>
  <!-- Router View -->
  <Navigation :toggles="['media']" @onToggleUpdate="handleToggleUpdate" />
  <router-view v-slot="{ Component }">
    <component :is="Component" :toggle_states="toggle_states" />
  </router-view>
</template>

<style scoped>
</style>