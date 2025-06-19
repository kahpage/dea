<!--============================================================ ...
     Event List tab
... ============================================================ -->

<style>
    @import '@/assets/common.css';
</style>

<script setup>
  import { ref } from "vue";
  import axiosInstance from '@/axios/axios_config.js';
  const baseUrl = import.meta.env.VITE_APP_BASE_URL;

  const loading_done = ref(false);
  const loaded_counter = ref(0);
  const loading_current = ref("");
  // const jsonData = ref([]);

  const public_path = import.meta.env.MODE == 'production' ? `/dea/` : `../`
  
  function fetch_db_index() {
    loading_done.value = false; 
    loaded_counter.value = 0; 
    loading_current.value = ''; // Reset
    axiosInstance.get( `${public_path}databases/database_file_index.json`)
      .then(response => {
        console.log(response.data);
        for (const db_name in response.data) {
          loading_current.value = db_name;
          if (fetch_db(response.data[db_name])) {loaded_counter.value++;} // increase IF loaded          
        }
        loading_done.value = true;
      })
      .catch(error => {
        console.error('Error fetching data:', error); // Log any errors that occur during the fetch
      });
  }

  function fetch_db(db_name) {
    // Return the promise chain
    return axiosInstance.get(`${public_path}databases/${db_name}/${db_name}.json`)
      .then(response => {
        console.log(response.data);
        return true; // TODO: not good enough check (check if valid json too ?)
      })
      .catch(error => {
        console.error('Error fetching data:', error); // Log any errors that occur during the fetch
        return false;
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

    <a v-if="!loading_done">
      <div class="header">Event list not yet loaded.</div>
      <div class="header">{{ loaded_counter }} loaded databases.</div>
      <div class="header" v-if="loading_current!==''">Fetching {{ loading_current }} ...</div>
    </a>
    <a v-else>
      <div class="header">Event list loaded ! ( {{ loaded_counter }} )</div>
    </a>
    <hr>

    
</template>


