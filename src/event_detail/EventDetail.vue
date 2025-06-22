<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import { ref, computed, watchEffect  } from "vue";
import { useRoute } from "vue-router";
import axiosInstance from "@/axios/axios_config.js";

const public_path = import.meta.env.MODE == "production" ? `/dea/` : `/dea/`; // Path of public/ folder

const route = useRoute();
const props = defineProps({
  db_path: String,
});

const db_path_args = computed(() => {
  return props.db_path ? props.db_path.split("/").filter(Boolean) : [];
});

const db_path_description = computed(() => {
  // file path description
  return db_path_args.value.slice(0, -1);
});

const db_path_event_name = computed(() => {
  // event entry inside the json
  return db_path_args.value.length > 0
    ? db_path_args.value[db_path_args.value.length - 1]
    : null;
});

const event_data = ref(null);

async function fetch_db() {
  // Construct the URL using the parameters
  event_data.value = {};
  let db_name = db_path_description.value[db_path_description.value.length - 1];
  let ar_path_more = [`${public_path}databases`]
    .concat(db_path_description.value)
    .concat([`${db_name}.json`]);
  let db_url = ar_path_more.join("/"); // complete path
  console.log(`Fetching ${db_url}...`); // Log the fetched data

  try {
    const response = await axiosInstance.get(db_url);
    if (!response.data.hasOwnProperty("aliases")) {
      return; // Check if the response is invalid
    }

    console.log("NEW FETCHED: ", response.data); // Log the fetched data
    return get_event_db(response.data);
  } catch (error) {
    console.error("Error fetching data:", error); // Log any errors that occur during the fetch
  }
}

function get_event_db(response_data) {
  if (!response_data.hasOwnProperty("events")) {
    return; // Check if the response is invalid
  }
  if (!Array.isArray(response_data["events"])) {
    return; // Check if the response is invalid
  }

  for (const cur_event of response_data["events"]) {
    if (
      !cur_event.hasOwnProperty("aliases") ||
      !Array.isArray(cur_event["aliases"])
    ) {
      continue; // Check if the response is invalid
    }
    if (!cur_event["aliases"].includes(db_path_event_name.value)) {
      continue;
    }

    event_data.value = cur_event;
    return;
  }
}

// Watch for changes in db_path_description and db_path_event_name
watchEffect(async () => {
  if (db_path_description.value && db_path_event_name.value) {
    console.log("Url change detected, now fetching new event data...")
    const data = await fetch_db(
      db_path_description.value,
      db_path_event_name.value
    );
  }
});
</script>

<template>
  <!-- Title -->
  <head>
    <title>dea | Event Detail</title>
  </head>

  <div class="header-title">Event detail</div>
  <div v-if="!props.db_path" class="header">
    Invalid database to fetch: "{{ props.db_path }}"
  </div>
  <div v-else>
    <div v-if="!event_data">Loading database {{ props.db_path }}...</div>
    <div v-else>
      <!-- event_data= {{ event_data }} -->
    </div>
  </div>

  <p>props.db_path = {{ props.db_path }}</p>
  <p>db_path_args = {{ db_path_args }}</p>
  <p>db_path_description = {{ db_path_description }}</p>
  <p>db_path_event_name = {{ db_path_event_name }}</p>
  <p>event_data = {{ event_data }}</p>
</template>

<style>
@import "@/assets/common.css";
</style>
