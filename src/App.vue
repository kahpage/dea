<script setup>
  import "./assets/app.css"
</script>

<template>
  <div id="app">
    <!-- Navigation Links -->
    <nav class="navigation">
      <router-link to="/" class="navigation-button">Home</router-link>
      <router-link to="/about" class="navigation-button">About</router-link>
    </nav>

    <!-- Router View -->
    <router-view class="content"/>
  </div>
</template>

<style scoped>

</style>
