<!--============================================================ ...
     App tab
... ============================================================ -->

<script setup>
  import "@/_assets/app.css"
  import Navigation from "@/_components/Navigation.vue"
  import EventList from "./EventList.vue"
</script>

<template>
  <!-- Router View -->
  <Navigation />
  <EventList />
  <a>Test</a>
  
</template>
