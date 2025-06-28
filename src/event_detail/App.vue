<!--============================================================ ...
     App tab
... ============================================================ -->

<script setup>
  import "@/assets/app.css"
  import Navigation from "@/components/Navigation.vue"
  import { ref } from 'vue'
</script>

<template>
  <!-- Router View -->
  <Navigation/>
  <router-view v-slot="{ Component }">
    <component :is="Component"/>
  </router-view>
</template>

<style scoped>
</style>