<!--============================================================ ...
     Calendar page
... ============================================================ -->

<script setup>
import Navigation from "@/components/Navigation.vue";
import YearTimeline from "./YearTimeline.vue";
import axiosInstance from "@/axios/axios_config.js";
import { computed, onMounted, ref } from "vue";

import { PATH_DB_EXPORTED, fetch_url } from "@/assets/utils.js";

const event_list_index = ref({});
const event_list_index_state = ref("loading"); // 'loading', 'loaded', 'error'
const year_oldest = ref(new Date().getFullYear()); // Init to current year
const year_newest = ref(year_oldest.value); // Init to current year

async function fetch_el_db() {
  fetch_url({
    url: [PATH_DB_EXPORTED].concat("event_list_index.json").join("/"),
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

function parse_event_dates(event) {
    const dates = event["dates"] || "";
    let date_start = null; // Start date [y, m, d]
    let date_end = null;   // End date   [y, m, d]
    let was_held = true;   // Whether the event was held

    const regex_date_range = /(\d{4})\.(\d{2})\.(\d{2})\s*-\s*(\d{4})\.(\d{2})\.(\d{2})/g;
    const matches = [...dates.matchAll(regex_date_range)];
    if (matches.length > 0) {  // Date range
        const last = matches[matches.length - 1];
        date_start = [parseInt(last[1]), parseInt(last[2]), parseInt(last[3])];
        date_end = [parseInt(last[4]), parseInt(last[5]), parseInt(last[6])];
    } else {                   // Single date
        const regex_single_date = /(\d{4})\.(\d{2})\.(\d{2})/g;
        const single_matches = [...dates.matchAll(regex_single_date)];
        if (single_matches.length > 0) {
            const last = single_matches[single_matches.length - 1];
            date_start = [parseInt(last[1]), parseInt(last[2]), parseInt(last[3])];
            date_end = [parseInt(last[1]), parseInt(last[2]), parseInt(last[3])];
        } else {
            // No valid date found
        }
    }
    // Check for cancellation keywords
    if (dates.toLowerCase().includes("cancelled")) {
        was_held = false;
    }
  
    return [date_start, date_end, was_held];
}

function recursive_flatten_event_groups(el_index, ar_path=[], hue_low=0, hue_high=360) {
    let flat_event_groups = {} // {year: [events of the year]}
    let subcategs = Object.keys(el_index).filter(k => k !== "@databases" && k !== "@count");
    let event_groups = el_index["@databases"] || {};

    let event_group_count = Object.keys(event_groups).length;
    let subcategs_count = subcategs.length;
    
    // == Hue ranges: [ @db | @sub categs ] ==
    let hue_high_db = hue_high;
    let hue_low_subcategs = hue_high;
    if (subcategs_count > 0 && event_group_count > 0) {
        hue_high_db = (hue_low + hue_high) * 0.5; // mid
        hue_low_subcategs = hue_high_db;
    } else if (subcategs_count > 0) {
        hue_low_subcategs = hue_low;
    } else if (event_group_count > 0) {
        hue_high_db = hue_high;
    } else { // No subcategs nor dbs
        return flat_event_groups;
    }

    // == Databases ==
    // Iterate over event groups with index
    for (const[index, [event_group_name, event_group]] of Object.entries(event_groups).entries()) {
        let event_group_events = event_group?.events;
        let event_group_ar_path = ar_path.concat([event_group_name]);
        let hue_event_group = hue_low + (hue_high_db - hue_low) * index / event_group_count;
        
        // Iterate over events
        for (const [event_name, event_data] of Object.entries(event_group_events)) {
            let [date_start, date_end, was_held] = parse_event_dates(event_data);
            if (date_start === null || date_end === null) {
                continue; // Skip events without valid dates
            }
            let year = date_start[0];
            if (!flat_event_groups.hasOwnProperty(year)) {
                flat_event_groups[year] = [];
            }
            let event = {
                  name: event_name,
                  date_start: date_start,
                  date_end: date_end,
                  was_held: was_held,
                  ar_path: event_group_ar_path,
                  hue: hue_event_group
              }
            flat_event_groups[year].push(event);
            // Update oldest and newest years
            if (year_oldest.value === null || year < year_oldest.value) {year_oldest.value = year;}
            if (year_newest.value === null || year > year_newest.value) {year_newest.value = year;}
        }
    }

    // == Sub categories ==
    for (const year of Object.keys(flat_event_groups)) {
        // Concatenate events from subcategories
        for (const key of subcategs) {
            const sub_flat = recursive_flatten_event_groups(
                el_index[key], ar_path.concat([key]), hue_low_subcategs, hue_high
            );
            if (!sub_flat.hasOwnProperty(year)) {
                flat_event_groups[year] = [];
            }
            flat_event_groups[year] = flat_event_groups[year].concat(sub_flat[year]);
        }
    }
    return flat_event_groups;
}

const el_flat_categories = computed(
    () => recursive_flatten_event_groups(event_list_index.value)
);

const dummy = computed(() => {
    console.log("Flattened event list:", el_flat_categories.value);
    return true;
});

/* Run fetch_event_list on component mount */
onMounted(async () => {
  await fetch_el_db();
});
</script>

<template>
  <!-- Title -->
  <head>
    <title>dea | Calendar</title>
  </head>

  <div class="el-container">
    <div class="el-content">
      <section id="top"></section>
      <Navigation />
      <div class="header-title">Calendar</div>
      <div class="header">Calendar of events in the database.</div>

      <div class="status-message" v-if="event_list_index_state === 'loading'">
        Fetching event list...
      </div>
      <div
        class="status-message"
        v-else-if="event_list_index_state === 'error'"
      >
        Failed to fetch event list.
        <button 
          class="retry-button"
          @click="fetch_el_db"
          title="Retry fetching event list."
        >
          Retry
        </button>
      </div>
      <div v-else>
        <!-- Successfully fetched event list -->
        <div v-for="year in Object.keys(el_flat_categories).sort((a,b) => b - a)" :key="year">
          <YearTimeline 
            :year="parseInt(year)" 
            :events_of_the_year="el_flat_categories[year]"
          />  

        </div>

      </div>
    </div>
  </div>
</template>

<style>
@import "@/assets/common.css";

/* .el-container {
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
} */
</style>
