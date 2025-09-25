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
import ToggleShow from "@/components/ToggleShow.vue";
import { useTemplateRef, markRaw } from "vue";

import PopUpManager from "@/components/PopUpManager.vue";
import MediaGrid from "@/components/MediaGrid.vue";
import PopUpCircledetails from "./PopUpCircledetails.vue";

const route = useRoute();
const props = defineProps({
  db_path: String,
});

const event_data = ref(null);
const event_data_state = ref("loading"); // 'loading', 'loaded', 'error'

async function fetch_db() {
  // Construct the URL using the parameters
  event_data.value = {};
  event_data_state.value = "loading";
  let db_url =
    [PATH_DB_EXPORTED].concat(db_path_args.value).join("/") + ".json";
  console.log(`Fetching ${db_url}...`); // Log the fetched data

  try {
    const response = await axiosInstance.get(db_url);
    if (!response.data.hasOwnProperty("aliases")) {
      throw new Error("Invalid data format: 'aliases' property missing");
    }

    console.log("NEW FETCHED: ", response.data); // Log the fetched data

    event_data.value = response.data;
    event_data_state.value = "loaded";
  } catch (error) {
    console.error("Error fetching data:", error); // Log any errors that occur during the fetch
    event_data_state.value = "error";
  }
}

const db_path_args = computed(() => {
  return props.db_path ? props.db_path.split("/").filter(Boolean) : [];
});

/* PopUpManager */
const popUpManager = useTemplateRef("popUpManager");
function popupCircleDetails(circle_db) {
  popUpManager.value.addPopup(markRaw(PopUpCircledetails), {
    circle_db: circle_db,
    db_path: db_path_args.value.slice(0, -1),
  });
}

// Watch for changes in db_path_description and db_path_event_name
watchEffect(async () => {
  if (db_path_args.value) {
    console.log("Url change detected, now fetching new event data...");
    const data = await fetch_db();
  }
});
</script>

<template>
  <!-- Title -->
  <head>
    <title v-if="event_data?.aliases">
      dea | Event Detail {{ " - " + event_data?.aliases?.join(" / ") }}
    </title>
    <title v-else>dea | Event Detail</title>
  </head>

  <div class="header-title">Event detail</div>
  <div class="ed-message" v-if="event_data_state == 'loading'">
    Loading database {{ props.db_path }}...
  </div>
  <div class="ed-message" v-else-if="event_data_state == 'error'">
    Failed to fetch event group data.
    <button
      class="ed-button"
      @click="fetch_db"
      title="Retry fetching event group data."
    >
      Retry
    </button>
  </div>
  <div v-else>
    <!-- ===== EVENT GROUP DB FETCHED ===== -->
    <div class="ed-div">
      <div v-if="event_data.hasOwnProperty('aliases')" class="ed-header">
        {{ event_data.aliases.join(" / ") }}
      </div>

      <a
        class="ed-parent"
        :href="
          [`/dea/event_group_detail/#`]
            .concat(db_path_args)
            .slice(0, -1)
            .join('/')
        "
      >
        Parent event group: {{ db_path_args[db_path_args.length - 2] }}
      </a>

      <div v-if="event_data?.dates" class="ed-dates">
        Dates: {{ event_data?.dates ?? "" }}
      </div>

      <div
        v-if="event_data?.links && Array.isArray(event_data.links)"
        class="ed-links"
      >
        Links:
        <span v-html="makeLinksClickable(event_data.links.join(', '))"></span>
      </div>

      <!-- ===== Description ===== -->
      <ToggleShow
        class="ts-description"
        :button_text="'Description'"
        v-if="event_data?.description"
        :default_hidden="false"
      >
        <div class="ts-description-div">
          <p v-for="(row, i) in event_data.description.split('\n')" :key="i">
            <span v-html="makeLinksClickable(row)"></span>
          </p>
        </div>
      </ToggleShow>

      <!-- ===== CIRCLE LIST ===== -->
      <div
        v-if="
          event_data?.circles &&
          Array.isArray(event_data.circles) &&
          event_data.circles.length > 0
        "
        class="table-div"
      >
        <table class="ed-table">
          <thead>
            <tr>
              <th colspan="5" class="ed-table-title">Participating circles</th>
            </tr>
            <tr>
              <th>Position</th>
              <th>Aliases</th>
              <th>Pen Names</th>
              <th>links</th>
              <th>details</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(circle, i) in event_data.circles" :key="i">
              <th>{{ circle?.position ?? "" }}</th>
              <th>
                <span
                  v-if="
                    circle &&
                    circle.hasOwnProperty('aliases') &&
                    Array.isArray(circle['aliases'])
                  "
                  >{{ circle?.aliases?.join(" / ") ?? "" }}</span
                >
              </th>
              <th>{{ circle?.pen_names?.join(" / ") ?? "" }}</th>
              <th>
                <span
                  v-html="makeLinksClickable(circle?.links?.join(', ') ?? '')"
                ></span>
              </th>
              <th>
                <button
                  class="ed-popup-button"
                  @click="popupCircleDetails(circle)"
                  title="Show circle details"
                >
                  🡵
                </button>
              </th>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ===== SOURCES ===== -->
    <ToggleShow
      class="ts-sources"
      :button_text="'Sources'"
      v-if="event_data?.sources"
    >
      <p v-for="(source_, i) in event_data.sources" :key="i">
        <span v-if="source_.type"
          >({{ source_.type[0] }}, {{ source_.type[1] }})
        </span>
        <span
          v-if="source_?.source"
          v-html="makeLinksClickable(source_.source)"
        ></span>
      </p>
    </ToggleShow>

    <!-- ===== Comments ===== -->

    <ToggleShow
      class="ed-comments"
      :button_text="'Comments'"
      v-if="event_data && event_data?.comments"
    >
      <p v-for="(row, i) in event_data.comments.split('\n')" :key="i">
        {{ row }}
      </p>
    </ToggleShow>

    <!-- ===== MEDIA ===== -->

    <ToggleShow class="ts-sources" :button_text="'Media'" v-if="event_data">
      <MediaGrid
        :media_list="event_data.media"
        :media_folder_path="
          [PATH_DB_TO_EXPORT]
            .concat(db_path_args.slice(0, -1))
            .concat('media')
            .join('/')
        "
      />
    </ToggleShow>
  </div>

  <PopUpManager ref="popUpManager" />
</template>

<style scoped>
@import "@/assets/common.css";

.ed-div {
  padding: 1em;
  background-color: var(--greyish-dark);
}

.ed-header {
  color: var(--scarlet-vibrant);
  font-weight: 700;
  font-size: x-large;
}

.table-div {
  width: 98vw;
  margin-top: 1em;
  overflow: hidden;
  border-radius: 0.7em;
}

.ed-table {
  width: 100%;
  font-size: 1em;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 1em rgba(59, 57, 57, 0.15);
  border: 0.2em solid var(--scarlet-dark);
  text-align: left;
  border-collapse: collapse;
  table-layout: auto;
}

.ed-table th,
.ed-table td {
  text-align: left;
  color: var(--grey-light);
  word-wrap: break-word;
  max-width: 45vw;
}

thead {
  background-color: var(--scarlet-dark);
  color: var(--grey-vibrant);
  text-align: left;
}

.ed-table-title {
  text-align: center !important;
  font-size: x-large;
  padding-bottom: 0.3em;
  background-color: var(--scarlet-dark);
  color: var(--grey-vibrant);
}

tbody tr:nth-child(odd) {
  background-color: var(--grey-dark);
}

.ts-sources {
  margin-left: 1em;
  width: min-content;
}

.ts-description {
  margin-left: -0.5em;
  max-width: 95%;
}

.ts-description-div {
  width: 95%;
}

.ts-description-div p {
  word-wrap: break-word;
}

.ed-popup-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--orange-light);
  font-weight: 900;
}

.ed-popup-button:hover {
  color: var(--orange-vibrant);
}

p {
  margin: 0;
}

.ed-button {
  background-color: var(--purple-deeper);
  color: var(--greyish-light);
  border: none;
  padding: 0.5em 1em;
  border-radius: 0.5em;
  cursor: pointer;
  box-shadow: 0 0 0.5em rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

.ed-message {
  padding: 0 1em;
  color: var(--purple-dark);
  font-size: medium;
}
</style>
