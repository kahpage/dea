<script setup>
import { useVirtualList } from "@vueuse/core";
import { computed, useTemplateRef, markRaw } from "vue";
import { asyncsleep, PATH_DB_EXPORTED } from "@/assets/utils.js";
import { ref } from "vue";
// import circle_raw_compact_index from "@/assets/static_databases/circle_participation_compact_index.json"; // Static database import
import PopUpManager from "@/components/PopUpManager.vue";
import PopUpCirclePartialdetails from "./PopUpCirclePartialdetails.vue";
import axiosInstance from "@/axios/axios_config.js";

const search_state = ref(["Disabled"]); // ["Disabled"], ["Loading", (int) current fetch counter | "parsing"], ["Enabled"], ["Error"]
let circle_raw_compact_index = {}; // Compact index variant
const keywords = ref("");
const circle_raw_extensive_index = ref({}); // Extensive index variant
const extensive_index_count = circle_raw_compact_index.hasOwnProperty("@extensive_chunk_count") ? circle_raw_compact_index["@extensive_chunk_count"] : null;

function recursive_fill_circle_extensive_index(current_raw_index, ar_path) {
  // Extensive index variant
  let current_circle_list = [];

  for (const key in current_raw_index) {
    if (Array.isArray(current_raw_index[key])) {
      /* Content is array: key is an event name */
      let raw = current_raw_index[key];
      for (const circle_i in raw) {
        raw[circle_i]["ar_path"] = ar_path.concat(key); // add ar_path
        raw[circle_i]["event_name"] = key; // add event name
      }

      current_circle_list = [].concat(current_circle_list, raw);
    } else {
      /* Content is object: folder, key is the folder name */
      let raw = recursive_fill_circle_extensive_index(
        current_raw_index[key],
        ar_path.concat(key)
      );
      current_circle_list = [].concat(current_circle_list, raw);
    }
  }

  return current_circle_list;
}
function recursive_fill_compact_circle_index(
  current_raw_compact_index,
  ar_path
) {
  // Compact index variant
  let current_circle_list = [];

  for (const key in current_raw_compact_index) {
    if (Array.isArray(current_raw_compact_index[key])) {
      /* Content is array: key is an event name */
      let raw = current_raw_compact_index[key];
      for (const circle_i in raw) {
        let circle = {
          ar_path: ar_path.concat(key), // add ar_path
          event_name: key, // add event name
          names: raw[circle_i], // add names
        };
        current_circle_list.push(circle);
      }
    } else {
      /* Content is object: folder, key is the folder name */
      let raw = recursive_fill_compact_circle_index(
        current_raw_compact_index[key],
        ar_path.concat(key)
      );
      current_circle_list = [].concat(current_circle_list, raw);
    }
  }

  return current_circle_list;
}

const circle_extensive_index = computed(() => {
  if (!circle_raw_extensive_index.value || !Object.keys(circle_raw_extensive_index.value).length) {
    return []; // Return empty array if no data is available
  }
  return recursive_fill_circle_extensive_index(circle_raw_extensive_index.value, []);
});

const circle_compact_index = computed(() => {
  return recursive_fill_compact_circle_index(circle_raw_compact_index, []);
});

const circle_index = computed(() => {
  if (search_state.value[0] === "Enabled") {
    // Extensive index
    return circle_extensive_index.value;
  } else {
    // Compact index
    return circle_compact_index.value;
  }
});

const circle_index_lowered = computed(() => {
  if (
    !circle_index ||
    !circle_index.value ||
    !Array.isArray(circle_index.value)
  ) {
    return [];
  }
  return circle_index.value.map((circle) => {
    return {
      ...circle,
      names: circle.names.map((name) => name.trim().toLowerCase()), // Lowercase all names
      misc:
        circle.misc && Array.isArray(circle.misc)
          ? circle.misc.map((name) => name.trim().toLowerCase())
          : null, // Lowercase all misc
      event_name: circle.event_name.trim().toLowerCase(), // Lowercase event name
    };
  });
});

const filtered_circles = computed(() => {
  // According to keywords
  if (
    !circle_index ||
    !circle_index.value ||
    !Array.isArray(circle_index.value)
  ) {
    return [];
  }

  let query = keywords.value.trim().toLowerCase();
  return circle_index.value.filter((circle, index) => {
    let circle_lowered = circle_index_lowered.value[index];
    let matchNames = circle_lowered.names.some((name) => name.includes(query)); // Check if any name in the circle's names array includes the search query
    let matchEvent = circle_lowered.event_name.toLowerCase().includes(query); // Check for event match
    let matchMisc =
      circle_lowered.misc &&
      circle_lowered.misc.some((misc) => misc.toLowerCase().includes(query));
    return matchNames || matchEvent || matchMisc; // Return true if either matches
  });
});

const { list, containerProps, wrapperProps, scrollTo } = useVirtualList(
  filtered_circles,
  {
    itemHeight: 10,
    // overscan: 10,
  }
);

function onSearchUpdate(event) {
  keywords.value = event.target.value;
  scrollTo(0);
}

/* Deep Search Activation */
function activateExtensiveSearch() {
  if (search_state.value[0] !== "Disabled" && search_state.value[0] !== "Error") {
    console.warn(
      "activateExtensiveSearch was called while Deep Search is already enabled or loading."
    );
    return; // Do not activate if already enabled or loading
  }

  search_state.value = ["Loading", 0];
  fetch_extensive_circle_index();
}
async function fetch_extensive_circle_index() {
  circle_raw_extensive_index.value = {}; // Reset the index
  // Construct the base URL
  let base_url = [PATH_DB_EXPORTED]
    .concat(["circle_participation_extensive_index.json"])
    .join("/");

  let raw_json = ""
  
  // For i in 0 extensive_index_count, console log i
  for (let i = 0; i < extensive_index_count; i++) {
    let part_url = `${base_url}_${i}`
    
    try {
      const response = await axiosInstance.get(part_url, {
        responseType: 'text' // Get raw text instead of parsed JSON
      });
      search_state.value = ["Loading", i]; // Set the state to enabled after fetching

      console.log(`NEW FETCHED: (${part_url})`, ); // Log the fetched data
      raw_json = raw_json + response.data; // Append content
    } catch (error) {
      search_state.value = ["Error"]; // Set the state to error if fetching fails
      console.error("Error fetching data:", error); // Log any errors that occur during the fetch
    }
  
  }
  search_state.value = ["Loading", "parsing"]; // Set the state to loading with the count of fetched parts

  await asyncsleep(1000); // wait 1 sec
  // Parse the concatenated JSON string
  try {
    circle_raw_extensive_index.value = JSON.parse(raw_json);
    search_state.value = ["Enabled"];
  } catch (error) {
    search_state.value = ["Error"];
    console.error("Error parsing concatenated JSON:", error);
  }
}

/* PopUpManager */
const popUpManager = useTemplateRef("popUpManager");
function popupCircleDetails(circle_partial_db) {
  // console.log("circle_partial_db :", circle_partial_db);
  popUpManager.value.addPopup(markRaw(PopUpCirclePartialdetails), {
    circle_db: circle_partial_db,
    db_path: circle_partial_db.ar_path,
  });
}
</script>

<template>
  <!-- Title -->
  <head>
    <title v-if="search_state[0] == 'Enabled'">
      dea | Circle Participation (extensive search)
    </title>
    <title v-else>dea | Circle Participation</title>
  </head>

  <div class="header-title">Circle Participation</div>
  <div class="header">
    List of participating circles in the database.
  </div>

  <div class="ds-header">
    <div v-if="search_state[0] == 'Disabled'">
      Circle extensive search is not enabled. Searching circle names and event names only.  <br />
      <button class="ds-button" @click="activateExtensiveSearch" title="Activating will download a rather large file.">
        Enable Circle Extensive Search
      </button>
    </div>
    <div v-if="search_state[0] == 'Error'">
      ERROR. Try again ?
      <button class="ds-button" @click="activateExtensiveSearch">
        Activate Circle Extensive Search
      </button>
    </div>
    <div v-if="search_state[0] == 'Loading'">
      Circle Extensive Search is loading (
        <span v-if="search_state[1] == 'parsing'">
          parsing extended circle index, might take a while ) ...
        </span>
        <span v-else>
          downloading <i>circle_participation_index.json_{{ search_state[1] }} / {{ extensive_index_count }}</i> ) ...
        </span>
    </div>
    <div v-if="search_state[0] == 'Enabled'">
      Circle Extensive Search is enabled. Now searching in more fields.
    </div>
  </div>

  <input
    class="cp-input"
    :value="keywords"
    @input="onSearchUpdate"
    placeholder="Keywords"
  />
  ({{ filtered_circles?.length }} results)

  <div class="cp-div">
    <table class="cp-header-table">
      <thead>
        <tr>
          <th colspan="4" class="cp-table-title">Participating circles</th>
        </tr>
        <tr>
          <th>Names / Pen Names</th>
          <th>Event</th>
        </tr>
      </thead>
    </table>

    <div class="cp-vlist">
      <div v-bind="containerProps" class="cp-vlist-component">
        <div v-bind="wrapperProps">
          <div v-for="(circle, i) in list" :key="i" class="cp-vlist-item">
            <div
              :class="
                circle.index % 2 === 0
                  ? 'cp-vlist-item-even'
                  : 'cp-vlist-item-odd'
              "
            >
              <!-- {{ circle }} -->
              <table>
                <tbody>
                  <tr>
                    <th>
                      <button
                        class="cp-popup-button"
                        @click="popupCircleDetails(circle.data)"
                        title="Show circle (partial) details"
                      >
                        🡵
                      </button>
                      {{ circle.data.names.join(" / ") }}
                    </th>
                    <th>
                      <a
                        class="cp-event-link"
                        :href="
                          ['/dea/event_detail/#']
                            .concat(circle.data.ar_path)
                            .join('/')
                        "
                      >
                        {{ circle.data.event_name }}
                      </a>
                    </th>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <PopUpManager ref="popUpManager" />
</template>

<style scoped>
@import "@/assets/common.css";

.cp-div {
  margin: 1em;
  background-color: var(--orange-dark);
  color: var(--grey-vibrant);
  text-align: left;
  font-size: 18px;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 20px #3b393926;
  border: 3px solid var(--orange-dark);
  border-radius: 5px;
}

.cp-header-table {
  width: 100%;
}

.cp-table-title {
  font-size: larger;
  text-align: center;
  font-weight: 700;
}

.cp-vlist {
  margin: 0 0.25em;
  /* background-color: red; */
}

.cp-vlist-component {
  height: 30em;
}

/* Color even cp-vlist-component based on index in vlist */
.cp-vlist-item {
  height: 22px;
  padding: 0;
  background-color: var(--grey-dark);
  color: var(--grey-light);
}

.cp-vlist-item-even {
}
.cp-vlist-item-odd {
  background-color: var(--greyish-deep);
}

.cp-input {
  margin-top: 1em;
  margin-left: 1em;
}

th:nth-child(2) {
  text-align: right;
  padding-right: 1em;
}

table {
  width: 100%;
}

tr {
  padding: 0 0.3em;
  color: var(--grey-light);
  width: 100%;
}

a.cp-event-link {
  color: var(--scarlet-soft);
}

.cp-popup-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--orange-light);
  font-weight: 900;
}

.cp-popup-button:hover {
  color: var(--orange-vibrant);
}

.ds-header {
  margin-left: 1rem;
  font-size: large;
  color: var(--purple-dark);
  font-family: "Segoe UI";
  font-weight: 500;
}

.ds-button {
  background-color: var(--purple-deeper);
  color: var(--greyish-light);
  border: none;
  padding: 0.5em 1em;
  border-radius: 0.5em;
  cursor: pointer;
  box-shadow: 0 0 0.5em rgba(0, 0, 0, 0.2);
  font-weight: 600;
}
</style>
