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

  const test_var = ref(0);
  const jsonData = ref([]);

  const public_path = import.meta.env.MODE == 'production' ? `/dea/` : `../`

  function test() {
    console.log(test_var);
    test_var.value++;
  }

  function fetch_data() {
    axiosInstance.get( `${public_path}databases/yougakudann/yougakudann.json`)
      .then(response => {
        console.log(response.data);
        jsonData.value = response.data;
      })
      .catch(error => {
        // Log any errors that occur during the fetch
        console.error('Error fetching data:', error);
      });
  }
</script>

<template>
    <!-- Title -->
    <head><title>dea | Event List</title></head>

    <div class="header">
      Here is the event list. To load it, click {{ test_var }}
      <button @click="fetch_data" class="button">Click</button>
    </div>
    
</template>


