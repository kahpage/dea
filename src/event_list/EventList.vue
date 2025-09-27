<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import EventCategory from "@/components/EventCategory.vue";
import EventListMenuCategory from "./EventListMenuCategory.vue";
import Navigation from "@/components/Navigation.vue"
import axiosInstance from "@/axios/axios_config.js";
import { onMounted, ref } from "vue";

import { PATH_DB_EXPORTED, fetch_url } from "@/assets/utils.js";

const event_list_index = ref({});
const event_list_index_state = ref('loading'); // 'loading', 'loaded', 'error'

async function fetch_el_db() {
  fetch_url({
    url: [PATH_DB_EXPORTED].concat('event_list_index.json').join("/"),
    axiosInstance: axiosInstance,
    on_start: () => {
      event_list_index.value = {};
      event_list_index_state.value = "loading";
    },
    on_success: (fetched_data) => {
      event_list_index.value = fetched_data;
      event_list_index_state.value = "loaded";
    },
    on_error: (error) => {
      event_list_index_state.value = "error";
    },
  });
}

/* Run fetch_event_list on component mount */
onMounted(async () => {
  await fetch_el_db();
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
      
      <div class="status-message" v-if="event_list_index_state === 'loading'">
        Fetching event list...
      </div>
      <div class="status-message" v-else-if="event_list_index_state === 'error'">
        Failed to fetch event list.
        <button class="retry-button" @click="fetch_event_list" title="Retry fetching event list.">
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

.retry-button {
  background-color: var(--purple-deeper);
  color: var(--greyish-light);
  border: none;
  padding: 0.5em 1em;
  border-radius: 0.5em;
  cursor: pointer;
  box-shadow: 0 0 0.5em rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

.status-message {
  padding: 0 1em;
  color: var(--purple-dark);
  font-size: medium;
}
</style>
