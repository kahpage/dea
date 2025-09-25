<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import EventCategory from "@/components/EventCategory.vue";
import EventListMenuCategory from "./EventListMenuCategory.vue";
import Navigation from "@/components/Navigation.vue"
import axiosInstance from "@/axios/axios_config.js";
import { onMounted, ref } from "vue";

import { PATH_DB_EXPORTED } from "@/assets/utils.js";

const event_list_index = ref({});
const event_list_index_state = ref('loading'); // 'loading', 'loaded', 'error'

async function fetch_event_list() {
  // Construct the URL
  event_list_index.value = {};
  event_list_index_state.value = 'loading';
  let db_url = [PATH_DB_EXPORTED].concat('event_list_index.json').join("/");
  console.log(`Fetching ${db_url}...`); // Log the fetched data

  try {
    const response = await axiosInstance.get(db_url);
    console.log("NEW FETCHED: ", response.data); // Log the fetched data
    
    event_list_index.value = response.data;
    event_list_index_state.value = 'loaded';

  } catch (error) {
    event_list_index_state.value = 'error';
    console.error("Error fetching data:", error); // Log any errors that occur during the fetch
  }
}

/* Run fetch_event_list on component mount */
onMounted(() => {
  fetch_event_list();
});
</script>

<template>
  <!-- event_list_index = {{ event_list_index }} -->

  <!-- Title -->
  <head>
    <title>dea | Event List</title>
  </head>

  <div class="el-container">
    <div class="el-content">
      <section id="top"></section>
      <Navigation/>
      <div class="header-title">Event list</div>
      <div class="header">A list of various events in the database.</div>
      
      <div class="el-message" v-if="event_list_index_state === 'loading'">
        Fetching event list...
      </div>
      <div class="el-message" v-else-if="event_list_index_state === 'error'">
        Failed to fetch event list.
        <button class="el-button" @click="fetch_event_list" title="Retry fetching event list.">
          Retry
        </button>
      </div>
      <div v-else>

      <EventCategory
        v-if="event_list_index !== undefined"
        :event_list_index="event_list_index"
        :ec_name="''"
        :ar_path="[]"
      />
      </div>
    </div>
    <div class="el-menu">
      <a class="el-menu-title" href="#top" title="Go Top">▲</a><span class="el-menu-title">Content</span>
      <EventListMenuCategory
        v-if="event_list_index !== undefined"
        :event_list_index="event_list_index"
        :ec_name="''"
      ></EventListMenuCategory>
    </div>
  </div>
</template>

<style>
@import "@/assets/common.css";

.el-container {
  display: flex;
  flex-direction: row;
  height: 100vh; 
  width: 100%; 
}

.el-content {
  flex: 1; 
  overflow-y: auto; 
  padding: 0;
  box-sizing: border-box;
}

.el-menu {
  width: 25%;
  background-color: var(--greyish-mild);
  padding-left: 0.5em;
  padding-top: 1em;
  height: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}

.el-menu-title {
  font-size: x-large;
  font-weight: 700;
  color: var(--purple-deep);
}
a.el-menu-title {
  font-size: medium;
  font-weight: 700;
  color: var(--purple-deep);
}

.el-button {
  background-color: var(--purple-deeper);
  color: var(--greyish-light);
  border: none;
  padding: 0.5em 1em;
  border-radius: 0.5em;
  cursor: pointer;
  box-shadow: 0 0 0.5em rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

.el-message {
  padding: 0 1em;
  color: var(--purple-dark);
  font-size: medium;
}
</style>
