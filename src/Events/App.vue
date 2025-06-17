<!--============================================================ ...
     App tab
... ============================================================ -->

<script setup>
  import "@/assets/app.css"
  import Navigation from "@/components/Navigation.vue"
  import EventList from "./EventList.vue"
</script>

<template>
  <!-- Router View -->
  <Navigation />
  <EventList />
  <a>Test</a>
  
</template>
