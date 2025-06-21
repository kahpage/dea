<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
  import { ref } from "vue";
  import axiosInstance from '@/axios/axios_config.js';
  import EventCategory from "./components/EventCategory.vue";

  import event_list_index from '@/assets/static_databases/event_list_index.json' // Static database import

  const baseUrl = import.meta.env.VITE_APP_BASE_URL;

  // const loaded_counter = ref(0); // Total databases loaded
  // const total = ref(0)           // Total databases registered in index
  // const database_file_index = ref({}); // Index content

  // const public_path = import.meta.env.MODE == 'production' ? `/dea/` : `../`
  
</script>

<template>
    <!-- Title -->
    <head><title>dea | Event List</title></head>

    <div class="header-title">Event list</div>
    <div class="header">A list of various events in the database.</div>

    <a>
      <!-- <div class="header"><span style="color: var(--greyish-soft)">{{ loaded_counter }} / {{ total }} event databases loaded.</span></div> -->
    </a>
    <hr>

    <EventCategory v-if="event_list_index !== undefined" :event_list_index="event_list_index" :ec_name="''"></EventCategory>

</template>

<style>
    @import '@/assets/common.css';
</style>