<!--============================================================ ...
     App tab
... ============================================================ -->

<script setup>
  import "@/assets/app.css"
  import Navigation from "@/components/Navigation.vue"
  
</script>

<template>
  <!-- Router View -->
  <Navigation />
  <router-view></router-view>
  
</template>
