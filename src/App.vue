<script setup>
  import "./assets/app.css"
</script>

<template>

  <!-- Navigation Links -->
  <nav class="navigation">
    <div class="navigation-buttons">
      <router-link to="/" class="navigation-button">Home</router-link>
      <router-link to="/about" class="navigation-button">About</router-link>
    </div>
    <div class="navigation-title"> dea</div>
  </nav>

  <!-- Router View -->
  <router-view class="content"/>
</template>

<style scoped>

</style>
