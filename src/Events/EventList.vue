<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
  import { ref } from "vue";
  import axiosInstance from '@/axios/axios_config.js';
  import EventCategory from "./components/EventCategory.vue";
  const baseUrl = import.meta.env.VITE_APP_BASE_URL;

  const loaded_counter = ref(0); // Total databases loaded
  const total = ref(0)           // Total databases registered in index
  const database_file_index = ref({}); // Index content

  const public_path = import.meta.env.MODE == 'production' ? `/dea/` : `../`
  
  function fetch_db_index() {
    axiosInstance.get( `${public_path}databases/database_file_index.json`)
      .then(response => {
        total.value = response.data["@count"]
        database_file_index.value = response.data;
      })
      .catch(error => {
        console.error('Error fetching data:', error); // Log any errors that occur during the fetch
      });
  }

  /* Load on page load */
  fetch_db_index();
</script>

<template>
    <!-- Title -->
    <head><title>dea | Event List</title></head>

    <div class="header-title">Event list</div>
    <div class="header">A list of various events in the database.</div>

    <a>
      <div class="header"><span style="color: var(--greyish-soft)">{{ loaded_counter }} / {{ total }} event databases loaded.</span></div>
    </a>
    <hr>

    <EventCategory v-if="database_file_index !== undefined" :event_categ_index="database_file_index" :ec_name="''" :ar_path="[]"></EventCategory>

</template>

<style>
    @import '@/assets/common.css';
</style>