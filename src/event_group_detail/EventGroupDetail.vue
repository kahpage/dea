<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import { ref, computed, watchEffect } from "vue";
import { useRoute } from "vue-router";
import axiosInstance from "@/axios/axios_config.js";
import {
  makeLinksClickable,
  PATH_DB_TO_EXPORT,
  PATH_DB_EXPORTED
} from "@/assets/utils.js";
import EventGroupTable from "@/components/EventGroupTable.vue";
import ToggleShow from "@/components/ToggleShow.vue";
import BarChart from "@/components/BarChart.vue";
import MediaGrid from "@/components/MediaGrid.vue";

const route = useRoute();
const props = defineProps({
  db_path: String,
});

const event_group_data = ref(null);
const event_group_data_state = ref("loading"); // 'loading', 'loaded', 'error'

async function fetch_db() {
  // Construct the URL using the parameters
  event_group_data.value = {};
  event_group_data_state.value = "loading";
  let ar_path_more = [PATH_DB_EXPORTED]
    .concat(db_path_args.value)
    .concat([`event_group.json`]);
  let db_url = ar_path_more.join("/"); // complete path
  console.log(`Fetching ${db_url}...`); // Log the fetched data

  try {
    const response = await axiosInstance.get(db_url);
    if (!response.data.hasOwnProperty("aliases")) {
      throw new Error("Invalid data format: 'aliases' property missing");
    }

    console.log("NEW FETCHED: ", response.data); // Log the fetched data
    if (!response.data.hasOwnProperty("aliases")) {
      throw new Error("Invalid data format: 'aliases' property missing");
    }
    event_group_data.value = response.data;
    event_group_data_state.value = "loaded";
  } catch (error) {
    event_group_data_state.value = "error";
    console.error("Error fetching data:", error); // Log any errors that occur during the fetch
  }
}

const media_list = computed(() => {
  if (
    !event_group_data.value ||
    !event_group_data.value.hasOwnProperty("media")
  ) {
    return [];
  }
  return event_group_data.value.media;
});

const db_path_args = computed(() => {
  return props.db_path ? props.db_path.split("/").filter(Boolean) : [];
});

// Watch for changes in db_path_args and db_path_event_name
watchEffect(async () => {
  if (db_path_args.value) {
    console.log("Url change detected, now fetching new event data...");
    const data = await fetch_db(db_path_args.value);
  }
});
</script>

<template>
  <!-- Title -->
  <head>
    <title v-if="event_group_data?.aliases">
      dea | Event Group Detail
      {{ " - " + event_group_data?.aliases?.join(" / ") }}
    </title>
    <title v-else>dea | Event Group Detail</title>
  </head>
  <div class="header-title">Event group detail</div>
  <div v-if="!props.db_path" class="header">
    Invalid database to fetch: "{{ props.db_path }}"
  </div>
  <div v-else>
    <div
      class="eg-message"
      v-if="
        event_group_data_state == 'loading'
      "
    >
      Loading database {{ props.db_path }}...
    </div>
    <div
      class="eg-message"
      v-else-if="event_group_data_state == 'error'"
    >
      Failed to fetch event group data.
      <button
        class="eg-button"
        @click="fetch_db"
        title="Retry fetching event group data."
      >
        Retry
      </button>
    </div>
    <div v-else>
      <!-- ===== EVENT GROUP DB FETCHED ===== -->
      <EventGroupTable
        :event_group_db="event_group_data"
        :eg_ar_path="db_path_args"
        :show_details="true"
      />

      <!-- ===== SOURCES ===== -->
      <ToggleShow
        class="ts-sources"
        :button_text="'Sources'"
        v-if="event_group_data?.sources"
      >
        <p v-for="(source_, i) in event_group_data.sources" :key="i">
          <span v-if="source_.type"
            >({{ source_.type[0] }}, {{ source_.type[1] }})
          </span>
          <span
            v-if="source_?.source"
            v-html="makeLinksClickable(source_.source)"
          ></span>
        </p>
      </ToggleShow>

      <!-- ===== LINKS ===== -->
      <ToggleShow
        class="ts-sources"
        :button_text="'Links'"
        v-if="event_group_data"
      >
        <div
          v-if="
            !event_group_data?.links ||
            Array.isArray(event_group_data?.links) &
              (event_group_data?.links == 0)
          "
        >
          (None)
        </div>
        <div class="ed-links">
          <div v-for="(link, index) in event_group_data?.links" :key="index">
            <span v-html="makeLinksClickable(link)"></span>
          </div>
        </div>
      </ToggleShow>

      <!-- ===== MEDIA ===== -->
      <ToggleShow
        class="ts-sources"
        :button_text="'Media'"
        v-if="event_group_data"
      >
        <MediaGrid
          :media_list="media_list"
          :media_folder_path="
            [PATH_DB_TO_EXPORT].concat(db_path_args).concat(['media']).join('/')
          "
        />
      </ToggleShow>

      <!-- ===== COMMENTS ===== -->
      <ToggleShow
        class="ts-comments"
        :button_text="'Comments'"
        v-if="event_group_data?.comments"
      >
        <p v-for="(row, i) in event_group_data.comments.split('\n')" :key="i">
          {{ row }}
        </p>
      </ToggleShow>

      <!-- Stats -->
      <ToggleShow
        class="ts-sources"
        :button_text="'Stats'"
        v-if="event_group_data?.events"
      >
        <BarChart
          :data="
            Object.keys(event_group_data.events).map((e) => ({
              value: event_group_data.events[e].circle_count,
              name: e,
            }))
          "
          :title="'Event participation'"
        />
      </ToggleShow>
    </div>
  </div>
</template>

<style scoped>
@import "@/assets/common.css";

.eg-button {
  background-color: var(--purple-deeper);
  color: var(--greyish-light);
  border: none;
  padding: 0.5em 1em;
  border-radius: 0.5em;
  cursor: pointer;
  box-shadow: 0 0 0.5em rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

.eg-message {
  padding: 0 1em;
  color: var(--purple-dark);
  font-size: medium;
}
</style>
