<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import { ref, computed, watchEffect } from "vue";
import { useRoute } from "vue-router";
import axiosInstance from "@/axios/axios_config.js";
import makeLinksClickable from "@/assets/utils.js";
import EventGroupTable from "@/components/EventGroupTable.vue";
import ToggleShow from "@/components/ToggleShow.vue";

const public_path = import.meta.env.MODE == "production" ? `/dea/` : `/dea/`; // Path of public/ folder

const route = useRoute();
const props = defineProps({
  db_path: String,
  toggle_states: Object,
});

const event_group_data = ref(null);

const do_show_media = computed(() => {
  if (!props.toggle_states || !props.toggle_states.hasOwnProperty("media")) {
    return false;
  }
  return props.toggle_states["media"];
});

const media_folder_path = computed(() => {
  return [`${public_path}databases`]
    .concat(db_path_args.value)
    .concat("media")
    .join("/");
});

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

async function fetch_db() {
  // Construct the URL using the parameters
  event_group_data.value = {};
  let db_name = db_path_args.value[db_path_args.value.length - 1];
  let ar_path_more = [`${public_path}databases`]
    .concat(db_path_args.value)
    .concat([`${db_name}.json`]);
  let db_url = ar_path_more.join("/"); // complete path
  console.log(`Fetching ${db_url}...`); // Log the fetched data

  try {
    const response = await axiosInstance.get(db_url);
    if (!response.data.hasOwnProperty("aliases")) {
      return; // Check if the response is invalid
    }

    console.log("NEW FETCHED: ", response.data); // Log the fetched data
    if (!response.data.hasOwnProperty("aliases")) {
      return;
    }
    event_group_data.value = response.data;
  } catch (error) {
    console.error("Error fetching data:", error); // Log any errors that occur during the fetch
  }
}

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
    <title>dea | Event Group Detail</title>
  </head>
  <div class="header-title">Event group detail</div>
  <div v-if="!props.db_path" class="header">
    Invalid database to fetch: "{{ props.db_path }}"
  </div>
  <div v-else>
    <div
      v-if="!event_group_data || !event_group_data.hasOwnProperty('aliases')"
    >
      Loading database {{ props.db_path }}...
    </div>
    <div v-else>
      <!-- ===== EVENT GROUP DB FETCHED ===== -->
      <EventGroupTable
        :event_group_db="event_group_data"
        :eg_ar_path="db_path_args"
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

      <!-- ===== MEDIA ===== -->

      <ToggleShow class="ts-sources" :button_text="'Media'" v-if="event_group_data">
        <div
          v-if="
            !media_list || Array.isArray(media_list) & (media_list.length == 0)
          "
        >
          (None)
        </div>
        <div class="ed-media">
          <div v-for="(media, index) in media_list" :key="index">
            <img
              :src="media_folder_path + '/' + media?.path"
              :alt="'Image ' + media.path"
              style="max-width: 100%; height: auto"
            />
            <div v-if="media.hasOwnProperty('sources')">
              <div v-for="(source_, j) in media?.sources" :key="j">
                <span v-if="source_.hasOwnProperty('type')"
                  >({{ source_["type"][0] }}, {{ source_["type"][1] }})</span
                >
                <br />
                <span v-html="makeLinksClickable(source_.source)"></span>
              </div>
            </div>
          </div>
        </div>
      </ToggleShow>
    </div>
  </div>
</template>

<style scoped>
@import "@/assets/common.css";
</style>
