<script setup>
import { useVirtualList } from "@vueuse/core";
import { computed, useTemplateRef, markRaw, onMounted } from "vue";
import { asyncsleep, PATH_DB_EXPORTED, fetch_url } from "@/assets/utils.js";
import { ref } from "vue";
import PopUpManager from "@/components/PopUpManager.vue";
import PopUpCirclePartialdetails from "./PopUpCirclePartialdetails.vue";
import axiosInstance from "@/axios/axios_config.js";
import ToggleSwitch from "@/components/ToggleSwitch.vue";

const keywords = ref("");
const query_input = ref(""); // immediate input shown to user (debounced into `keywords`)
const debounce_ms = 180; // debounce delay for search
let debounce_timer = null;
const metadata = ref({});
const circle_compact_index_parts = ref([]); // Fetched compact index parts
const circle_extensive_index_parts = ref([]); // Fetched extensive index parts
const circle_compact_index = ref([]);
const circle_extensive_index = ref([]);
const index_state = ref(["Idle"]);
const use_regex = ref(false); // Whether to use regex search or not

/* Fetch circle index metadata */
async function fetch_metadata() {
  fetch_url({
    url: [PATH_DB_EXPORTED].concat([`circle_index_metadata.json`]).join("/"),
    axiosInstance: axiosInstance,
    on_start: () => {
      metadata.value = {};
      index_state.value = ["Loading"];
    },
    on_success: (fetched_data) => {
      metadata.value = fetched_data;
      index_state.value = ["Loaded"];
    },
    on_error: (error) => {
      index_state.value = ["Error"];
    },
  });
}

/* Fetch circle raw indexes */
async function fetch_circle_raw_indexes(variant) {
  /* Initialize */
  let base_url = "";
  let index_count = 0;
  let index_parts_ptr = null;
  let index_ptr = null;
  if (variant == "compact") {
    // For compact only
    index_parts_ptr = circle_compact_index_parts;
    index_ptr = circle_compact_index;
    base_url = [PATH_DB_EXPORTED]
      .concat(["circle_participation_compact_index"])
      .join("/");
    index_count = metadata.value?.compact_index_chunk_count || 0;
    index_state.value = ["cLoading", 0];
  } else if (variant == "extensive") {
    index_parts_ptr = circle_extensive_index_parts;
    index_ptr = circle_extensive_index;
    base_url = [PATH_DB_EXPORTED]
      .concat(["circle_participation_extensive_index"])
      .join("/");
    index_count = metadata.value?.extensive_index_chunk_count || 0;
    index_state.value = ["eLoading", 0];
  } else {
    console.error("fetch_circle_raw_indexes: Unknown variant", variant);
    return;
  }
  index_parts_ptr.value = []; // Reset parts

  /* Fetch all parts */
  if (index_parts_ptr.value.length > 0) {
    console.log(
      `Retrying from ${index_parts_ptr.value.length} / ${index_count} for ${variant} index.`
    );
  }
  for (let i = index_parts_ptr.value.length; i < index_count; i++) {
    let part_url = `${base_url}_${i}.json`;

    try {
      const response = await axiosInstance.get(part_url, {
        responseType: "json", // Get raw text instead of parsed JSON
      });
      index_state.value[1] = i + 1; // Update the state

      console.log(`NEW FETCHED: (${part_url})`); // Log the fetched data
      index_parts_ptr.value.push(response.data); // Append content
    } catch (error) {
      index_state.value = [variant == "compact" ? "cError" : "eError"]; // Set the state to error if fetching fails
      console.error("Error fetching data:", error); // Log any errors that occur during the fetch
      return;
    }
  }

  /* Parse the concatenated JSON string */
  index_state.value = [variant == "compact" ? "cParsing" : "eParsing", 0];
  await asyncsleep(10); // wait a bit

  /* Fill circle index */
  index_ptr.value = [];
  for (let i = 0; i < index_parts_ptr.value.length; i++) {
    index_ptr.value = index_ptr.value.concat(
      recursive_fill_circle_indexes(index_parts_ptr.value[i], [], variant)
    );
    index_state.value[1] = i + 1; // Update the state
    // await asyncsleep(1); // wait a bit to allow UI updates
  }

  // Build compact lowercased search index in parallel (saves ~50%+ memory
  // compared to duplicating full objects). This is used for fast substring
  // and regex searches without touching original objects.
  try {
    search_index.value = build_search_index_for(index_ptr.value);
  } catch (e) {
    console.error("Error building search index:", e);
    search_index.value = [];
  }

  index_state.value = [variant == "compact" ? "cLoaded" : "eLoaded"];

  return;
}

function recursive_fill_circle_indexes(
  raw_index,
  ar_path = [],
  variant = "compact"
) {
  // variant: "compact" | "extensive"
  let current_circle_list = [];

  for (const key in raw_index) {
    if (Array.isArray(raw_index[key])) {
      /* Content is array: key is an event name */
      let event_circles = [];
      for (const circle_i in raw_index[key]) {
        // Add ar_path and event_name to each circle entry
        let raw_circle = raw_index[key][circle_i];
        let circle_to_add =
          variant == "extensive" ? raw_circle : { names: raw_circle };
        circle_to_add["ar_path"] = ar_path.concat(key); // add ar_path
        circle_to_add["event_name"] = key; // add event name
        event_circles.push(circle_to_add);
      }

      current_circle_list = [].concat(current_circle_list, event_circles);
    } else {
      /* Content is object: folder, key is the folder name */
      let raw = recursive_fill_circle_indexes(
        raw_index[key],
        ar_path.concat(key),
        variant
      );
      current_circle_list = [].concat(current_circle_list, raw);
    }
  }

  return current_circle_list;
}

const regex_expr = computed(() => {
  // Only build regex when regex mode is enabled and there is a pattern.
  if (!use_regex.value) return null;
  const k = keywords.value;
  if (!k || k.length === 0) return null;
  try {
    return new RegExp(k, "i"); // 'i' for case-insensitive
  } catch (e) {
    return null; // Invalid regex
  }
});

const circle_index = computed(() => {
  if (
    index_state.value[0] === "cLoaded" &&
    circle_compact_index &&
    circle_compact_index.value &&
    Array.isArray(circle_compact_index.value)
  ) {
    // Compact index
    return circle_compact_index.value;
  } else if (
    index_state.value[0] === "eLoaded" &&
    circle_extensive_index &&
    circle_extensive_index.value &&
    Array.isArray(circle_extensive_index.value)
  ) {
    // Extensive index
    return circle_extensive_index.value;
  } else {
    return [];
  }
});

// Compact, lower-cased search strings (one per circle) to avoid duplicating
// circle objects in memory. Each string contains event, names and misc
// joined with tabs, trimmed and lowercased.
const search_index = ref([]);

function build_search_index_for(arr) {
  if (!arr || !Array.isArray(arr)) return [];
  return arr.map((circle) => {
    const event = (circle.event_name || "").toString().trim();
    const names = Array.isArray(circle.names)
      ? circle.names.map((n) => n.toString().trim()).join(" / ")
      : (circle.names || "").toString().trim();
    const misc = Array.isArray(circle.misc)
      ? circle.misc.map((m) => m.toString().trim()).join(" / ")
      : (circle.misc || "").toString().trim();
    // Join parts with a separator and lowercase once.
    return [event, names, misc].filter(Boolean).join("\t").toLowerCase();
  });
}

const filtered_circles = computed(() => {
  // According to keywords
  if (
    !circle_index ||
    !circle_index.value ||
    !Array.isArray(circle_index.value)
  ) {
    return [];
  }
  const query = keywords.value.trim().toLowerCase();

  // If empty query, return whole index (no filtering) — avoids scanning everything.
  if (!query && !use_regex.value) return circle_index.value;

  return circle_index.value.filter((circle, index) => {
    const searchText = (search_index.value[index] || "").toString();

    if (use_regex.value) {
      if (!query) return false; // no pattern provided
      if (!regex_expr.value) return false; // invalid regex
      return regex_expr.value.test(searchText);
    }

    // Simple substring search on the compact lowercased string.
    return searchText.includes(query);
  });
});

const { list, containerProps, wrapperProps, scrollTo } = useVirtualList(
  filtered_circles,
  {
    itemHeight: 22,
    // overscan: 10,
  }
);

function onSearchUpdate(event) {
  const v = event.target.value;
  // update immediate input so the UI stays responsive
  query_input.value = v;

  // debounce actual search value to avoid running heavy filters on every keystroke
  if (debounce_timer) clearTimeout(debounce_timer);
  debounce_timer = setTimeout(() => {
    keywords.value = v;
    // reset virtual list scroll to top on new search
    scrollTo(0);
  }, debounce_ms);
}

// Export the currently filtered circles as a CSV file and trigger a download
function dumpFilteredCircles() {
  if (
    !filtered_circles ||
    !filtered_circles.value ||
    filtered_circles.value.length === 0
  )
    return;
  const rows = filtered_circles.value || [];

  function esc(v) {
    if (v === null || v === undefined) return "";
    return `"${String(v)
      .replace(/"/g, '""')
      .replace(/\t/g, "\\t")
      .replace(/\r?\n/g, "\\n")}"`;
  }

  const header = ["event_name", "names", "misc"];
  const csvLines = [header.join("\t")];

  for (const c of rows) {
    const event_name = c.event_name ?? "";
    const names = Array.isArray(c.names) ? c.names.join(" / ") : c.names ?? "";
    const misc = Array.isArray(c.misc) ? c.misc.join(" / ") : c.misc ?? "";
    csvLines.push([esc(event_name), esc(names), esc(misc)].join("\t"));
  }

  // Create file and trigger download
  const csv = csvLines.join("\r\n");
  const blob = new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `circle_search_dump.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
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

/* Run fetch_compact_circle_db on component mount */
onMounted(async () => {
  await fetch_metadata();
});
</script>

<template>
  <!-- Title -->
  <head>
    <title v-if="index_state[0] == 'eEnabled'">
      dea | Circle Participation (extensive search)
    </title>
    <title v-else>dea | Circle Participation</title>
  </head>

  <div class="header-title">Circle Participation</div>
  <div class="header">List of participating circles in the database.</div>

  <div v-if="index_state[0] == 'Loading'" class="status-message">
    Loading circle index metadata...
  </div>
  <div v-else-if="index_state[0] == 'Loaded'" class="status-message">
    Successfully loaded circle index metadata. One of the circle indexes can now
    be downloaded.
  </div>
  <div v-if="index_state[0] == 'cLoading'" class="status-message">
    Loading Compact Circle Index... Downloaded {{ index_state[1] }} /
    {{ metadata?.compact_index_chunk_count }}...
  </div>
  <div v-if="index_state[0] == 'cParsing'" class="status-message">
    Parsing Compact Circle Index... Parsed {{ index_state[1] }} /
    {{ metadata?.compact_index_chunk_count }}...
  </div>
  <div v-if="index_state[0] == 'cLoaded'" class="status-message">
    Successfully loaded Compact Circle Index.
  </div>
  <div v-if="index_state[0] == 'eLoading'" class="status-message">
    Loading Extensive Circle Index... Downloaded {{ index_state[1] }} /
    {{ metadata?.extensive_index_chunk_count }}...
  </div>
  <div v-if="index_state[0] == 'eParsing'" class="status-message">
    Parsing Extensive Circle Index... Parsed {{ index_state[1] }} /
    {{ metadata?.extensive_index_chunk_count }}...
  </div>
  <div v-if="index_state[0] == 'eLoaded'" class="status-message">
    Successfully loaded Extensive Circle Index.
  </div>
  <div v-else-if="index_state[0].endsWith('Error')" class="status-message">
    <!-- buttons -->
    Failed to fetch
    {{
      index_state[0] == "cError"
        ? "circle compact index"
        : index_state[0] == "eError"
        ? "circle extensive index"
        : "circle index metadata"
    }}.
    <button
      class="retry-button"
      @click="
        index_state[0] == 'Error'
          ? fetch_metadata()
          : index_state[0] == 'cError'
          ? fetch_circle_raw_indexes('compact')
          : fetch_circle_raw_indexes('extensive')
      "
      title="Retry fetching circle compact index."
    >
      Retry
    </button>
  </div>

  <!-- Load Buttons -->
  <div class="load-controls-row status-message">
    <div class="load-controls-left">
      <button
        v-if="index_state[0] == 'Loaded'"
        class="retry-button"
        @click="fetch_circle_raw_indexes('compact')"
        :title="`Load compact circle index (${
          metadata?.compact_index_chunk_count ?? 0
        } chunks, ${Math.ceil(
          (metadata?.compact_total_size || 0) / 1048576
        )} MB)`"
      >
        Compact circle index
      </button>

      <button
        v-if="index_state[0] == 'Loaded' || index_state[0] == 'cLoaded'"
        class="retry-button"
        @click="fetch_circle_raw_indexes('extensive')"
        :title="`Load extensive circle index (${
          metadata?.extensive_index_chunk_count ?? 0
        } chunks, ${Math.ceil(
          (metadata?.extensive_total_size || 0) / 1048576
        )} MB)`"
      >
        Extensive circle index
      </button>
    </div>

    <div class="load-controls-right">
      <button
        class="ds-button"
        @click="dumpFilteredCircles()"
        title="Dump search results to csv."
      >
        Dump search results
      </button>
    </div>
  </div>

  <div class="cp-div">
    <div class="cp-search-row" style="margin-bottom: 0.5em">
      <input
        class="cp-input"
        v-model="query_input"
        @input="onSearchUpdate"
        placeholder="Keywords"
      />

      <div class="cp-input cp-regex-group">
        <div class="cp-regex-label">Use Regex ?</div>
        <ToggleSwitch
          v-model:toggle_value="use_regex"
          :titleFunc="
            (state) =>
              state ? 'regex search enabled' : 'regex search disabled'
          "
        />
      </div>

      <div class="cp-results">({{ filtered_circles?.length }} results)</div>
    </div>
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
        <div v-bind="wrapperProps" class="cp-vlist-wrapper">
          <!-- The wrapper receives the total scroll height from `useVirtualList`.
               Inside it we absolutely-position visible items using vitem.start
               so the wrapper's height doesn't push the page scrollbar. -->
          <div
            v-for="vitem in list"
            :key="vitem.index"
            :class="[
              'cp-vlist-item',
              vitem.index % 2 === 0
                ? 'cp-vlist-item-even'
                : 'cp-vlist-item-odd',
            ]"
            class="cp-row"
            :style="{
              transform: `translateY(${vitem.start}px)`,
              height: '22px',
              willChange: 'transform',
            }"
          >
            <div class="cp-row-inner">
              <div class="cp-row-col cp-row-col-names">
                <button
                  class="cp-popup-button"
                  @click="popupCircleDetails(vitem.data)"
                  title="Show circle (partial) details"
                >
                  🡵
                </button>
                {{
                  Array.isArray(vitem.data.names)
                    ? vitem.data.names.join(" / ")
                    : vitem.data.names || ""
                }}
              </div>
              <div class="cp-row-col cp-row-col-event">
                <a
                  class="cp-event-link"
                  :href="
                    ['/dea/event_detail/#'].concat(vitem.data.ar_path).join('/')
                  "
                >
                  {{ vitem.data.event_name }}
                </a>
              </div>
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

/* Container and header */
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
}

/* The vlist container must be the scroll container. Keep a single definition. */
.cp-vlist-component {
  height: 30em;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  box-sizing: border-box;
}

/* Color rows and keep fixed height to match useVirtualList itemHeight */
.cp-vlist-item {
  height: 22px;
  padding: 0;
  background-color: var(--grey-dark);
  color: var(--grey-light);
}
.cp-vlist-wrapper {
  display: block;
  position: relative;
  width: 100%;
}

.cp-row {
  box-sizing: border-box;
}
.cp-row-inner {
  display: flex;
  align-items: center;
  height: 22px;
}
.cp-row-col {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding: 0 0.3em;
  line-height: 22px;
}
.cp-row-col-names {
  flex: 1 1 auto;
  text-align: left;
}
.cp-row-col-event {
  width: 20%;
  text-align: right;
}

/* Tables used by vlist */
.cp-vlist-component table,
.cp-body-table {
  table-layout: fixed;
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
}
.cp-body-table tbody tr.cp-vlist-item {
  height: 22px !important;
}
.cp-body-table td,
.cp-body-table th,
.cp-vlist-item td,
.cp-vlist-item th {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding: 0 0.3em;
  line-height: 22px;
  height: 22px;
}
.cp-vlist-item-even {
  background-color: var(--grey-dark);
}
.cp-vlist-item-odd {
  background-color: var(--greyish-deep);
}

.cp-input {
  margin-top: 1em;
  margin-left: 1em;
}
input.cp-input {
  background-color: var(--grey-vibrant);
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0.4em 0.6em;
  border-radius: 0.25em;
}

.cp-search-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.cp-search-row .cp-input {
  margin-top: 0;
  margin-left: 0;
}
.cp-regex-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  font-weight: 700;
  margin-left: 0.25rem;
}
.cp-regex-label {
  font-size: 0.95rem;
  line-height: 1;
}
.cp-results {
  margin-left: 0.25rem;
  font-weight: 600;
}

.load-controls-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin: 0.5em 1em;
}
.load-controls-left {
  display: flex;
  gap: 0.5rem;
}
.load-controls-right {
  display: flex;
  justify-content: flex-end;
}

th:nth-child(2) {
  text-align: right;
  padding-right: 1em;
}
table {
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
