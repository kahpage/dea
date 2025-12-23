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
  let date_end = null; // End date   [y, m, d]
  let was_held = true; // Whether the event was held

  const regex_date_range =
    /(\d{4})\.(\d{2})\.(\d{2})\s*-\s*(\d{4})\.(\d{2})\.(\d{2})/g;
  const matches = [...dates.matchAll(regex_date_range)];
  if (matches.length > 0) {
    // Date range
    const last = matches[matches.length - 1];
    date_start = [parseInt(last[1]), parseInt(last[2]), parseInt(last[3])];
    date_end = [parseInt(last[4]), parseInt(last[5]), parseInt(last[6])];
  } else {
    // Single date
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

function collect_event_groups(el_index, ar_path = []) {
  let event_groups_list = []; // Array of {key, name, ar_path, link, events}
  
  let subcategs = Object.keys(el_index).filter(
    (k) => k !== "@databases" && k !== "@count"
  );
  subcategs.sort((a, b) => a.localeCompare(b));
  
  let event_groups = el_index["@databases"] || {};
  
  // Sort event groups deterministically by their display name (alias) or key
  const event_group_entries = Object.entries(event_groups).sort(([, a], [, b]) => {
    const nameA = (a && a.aliases && a.aliases[0]) || "";
    const nameB = (b && b.aliases && b.aliases[0]) || "";
    if (nameA && nameB) return nameA.localeCompare(nameB);
    return String((a && a.key) || "").localeCompare(String((b && b.key) || ""));
  });
  
  // == Collect event groups (without hue assignment) ==
  for (const [event_group_key, event_group] of event_group_entries) {
    let event_group_ar_path = ar_path.concat([event_group_key]);
    let event_group_name = event_group.aliases[0];
    let pathStr = event_group_ar_path.join("/");
    
    event_groups_list.push({
      key: event_group_key,
      name: event_group_name,
      ar_path: event_group_ar_path,
      link: "/dea/event_group_detail/#/" + pathStr,
      events: event_group?.events || {}
    });
  }
  
  // == Sub categories ==
  for (const key of subcategs) {
    const sub_groups = collect_event_groups(
      el_index[key],
      ar_path.concat([key])
    );
    event_groups_list = event_groups_list.concat(sub_groups);
  }
  
  return event_groups_list;
}

const all_event_groups = computed(() => {
  const groups = collect_event_groups(event_list_index.value);
  
  // Assign hues sequentially in increasing order (0 to 360)
  const total = groups.length;
  return groups.map((group, index) => ({
    ...group,
    hue: total > 0 ? (360 * index) / total : 0
  }));
});

const el_flat_categories = computed(() => {
  const flat_event_groups = {}; // {year: [events of the year]}
  const event_groups = all_event_groups.value;
  
  for (const event_group of event_groups) {
    const event_group_name = event_group.name;
    const event_group_ar_path = event_group.ar_path;
    const hue_event_group = event_group.hue;
    const event_group_events = event_group.events;
    
    // Sort events by start date, then name
    const event_entries = Object.entries(event_group_events).sort(([nameA, dataA], [nameB, dataB]) => {
      const [startA] = parse_event_dates(dataA);
      const [startB] = parse_event_dates(dataB);
      if (startA && startB) {
        for (let i = 0; i < 3; i++) {
          const diff = (startA[i] || 0) - (startB[i] || 0);
          if (diff !== 0) return diff;
        }
        return nameA.localeCompare(nameB);
      } else if (startA) {
        return -1;
      } else if (startB) {
        return 1;
      }
      return nameA.localeCompare(nameB);
    });
    
    for (const [event_name, event_data] of event_entries) {
      let [date_start, date_end, was_held] = parse_event_dates(event_data);
      if (date_start === null || date_end === null) {
        continue; // Skip events without valid dates
      }
      let year_start = date_start[0];
      let year_end = date_end[0];
      if (year_start > year_end) {
        console.warn(
          `Event "${event_name}" has start year greater than end year: ${year_start} > ${year_end}. Skipping.`
        );
        continue;
      }
      
      // Handle events spanning multiple years
      if (year_start !== year_end) {
        for (let year = year_start; year <= year_end; year++) {
          if (!flat_event_groups.hasOwnProperty(year)) {
            flat_event_groups[year] = [];
          }
          let date_start_year = year === year_start ? date_start : [year, 1, 1];
          let date_end_year = year === year_end ? date_end : [year, 12, 31];
          let event = {
            name: event_name,
            raw_dates: event_data["dates"] || "",
            date_start: date_start_year,
            date_end: date_end_year,
            was_held: was_held,
            ar_path: event_group_ar_path,
            event_group_name: event_group_name,
            hue: hue_event_group
          };
          flat_event_groups[year].push(event);
        }
      } else {
        // Event within a single year
        if (!flat_event_groups.hasOwnProperty(year_start)) {
          flat_event_groups[year_start] = [];
        }
        let event = {
          name: event_name,
          raw_dates: event_data["dates"] || "",
          date_start: date_start,
          date_end: date_end,
          was_held: was_held,
          ar_path: event_group_ar_path,
          event_group_name: event_group_name,
          hue: hue_event_group
        };
        flat_event_groups[year_start].push(event);
      }
      
      // Update oldest and newest years
      if (year_oldest.value === null || year_start < year_oldest.value) {
        year_oldest.value = year_start;
      }
      if (year_newest.value === null || year_end > year_newest.value) {
        year_newest.value = year_end;
      }
    }
  }
  
  return flat_event_groups;
});

const legendItems = computed(() => {
  return all_event_groups.value.map(group => ({
    name: group.name,
    hue: group.hue,
    link: group.link
  }));
});

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

  <div class="ca-container">
    <div class="ca-content">
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
        <!-- Legend -->
        <div class="legend-container">
          <a
            v-for="item in legendItems"
            :key="item.name"
            :href="item.link"
            class="legend-item"
          >
            <div
              class="legend-color"
              :style="{ backgroundColor: `hsl(${item.hue}, 70%, 40%)` }"
            ></div>
            <span class="legend-text">{{ item.name }}</span>
          </a>
        </div>

        <!-- Timelines -->
        <div
          v-for="year in Object.keys(el_flat_categories).sort((a, b) => b - a)"
          :key="year"
        >
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

.ca-container {
  display: flex;
  flex-direction: row;
  height: 100vh;
  width: 100%;
}

.ca-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  box-sizing: border-box;
}

.ca-menu {
  width: 25%;
  background-color: var(--greyish-mild);
  padding-left: 0.5em;
  padding-top: 1em;
  height: 100%;
  overflow-y: auto;
  box-sizing: border-box;
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

.legend-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1em;
  margin: 1em 2em;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5em;
  text-decoration: none;
  cursor: pointer;
}

.legend-item:hover .legend-text {
  text-decoration: underline;
}

.legend-color {
  width: 1em;
  height: 1em;
  border-radius: 50%;
}

.legend-text {
  color: var(--grey-mild);
  font-size: 0.9em;
}
</style>
