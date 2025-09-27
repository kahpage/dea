<script setup>
import { useVirtualList } from "@vueuse/core";
import { computed, useTemplateRef, markRaw, onMounted } from "vue";
import { asyncsleep, PATH_DB_EXPORTED, fetch_url } from "@/assets/utils.js";
import { ref } from "vue";
// import circle_raw_compact_index from "@/assets/static_databases/circle_participation_compact_index.json"; // Static database import
import PopUpManager from "@/components/PopUpManager.vue";
import PopUpCirclePartialdetails from "./PopUpCirclePartialdetails.vue";
import axiosInstance from "@/axios/axios_config.js";
import ToggleSwitch from "@/components/ToggleSwitch.vue";

const keywords = ref("");
const metadata = ref({});
const raw_jsons = ref({ compact: [], extensive: [] }); // Raw JSON parts
const circle_raw_compact_index = ref({}); // Compact index variant
const circle_raw_extensive_index = ref({}); // Extensive index variant
const circle_compact_index = ref([]);
const circle_extensive_index = ref([]);
const index_state = ref(["Idle"]);
// None (metadata only): ["Loading"], // ["Loading"], ["Loaded"], ["Error"]
// compact: ["cLoading", (int) current fetch counter], ["cParsing"], ["cLoaded"], ["cError"]
// extensive: ["eLoading", (int) current fetch counter'], ["eParsing"], ["eLoaded"], ["eError"]

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
  let raw_index_ptr = null;
  let index_ptr = null;
  if (variant == "compact") {
    // For compact only
    raw_index_ptr = circle_raw_compact_index;
    index_ptr = circle_compact_index;
    base_url = [PATH_DB_EXPORTED]
      .concat(["circle_participation_compact_index.json_"])
      .join("/");
    index_count = metadata.value?.compact_index_chunk_count || 0;
    index_state.value = ["cLoading", 0];
  } else if (variant == "extensive") {
    raw_index_ptr = circle_raw_extensive_index;
    index_ptr = circle_extensive_index;
    base_url = [PATH_DB_EXPORTED]
      .concat(["circle_participation_extensive_index.json_"])
      .join("/");
    index_count = metadata.value?.extensive_index_chunk_count || 0;
    index_state.value = ["eLoading", 0];
  } else {
    console.error("fetch_circle_raw_indexes: Unknown variant", variant);
    return;
  }
  raw_index_ptr.value = {}; // Reset the index

  /* Fetch all parts */
  if (raw_jsons.value[variant].length > 0) {
    console.log(
      `Retrying from ${raw_jsons.value[variant].length} / ${index_count} for ${variant} index.`
    );
  }
  for (let i = raw_jsons.value[variant].length; i < index_count; i++) {
    let part_url = `${base_url}${i}`;

    try {
      const response = await axiosInstance.get(part_url, {
        responseType: "text", // Get raw text instead of parsed JSON
      });
      index_state.value[1] = i + 1; // Update the state

      console.log(`NEW FETCHED: (${part_url})`); // Log the fetched data
      raw_jsons.value[variant].push(response.data); // Append content
    } catch (error) {
      index_state.value = [variant == "compact" ? "cError" : "eError"]; // Set the state to error if fetching fails
      console.error("Error fetching data:", error); // Log any errors that occur during the fetch
      return;
    }
  }

  /* Parse the concatenated JSON string */
  index_state.value = [variant == "compact" ? "cParsing" : "eParsing"];
  await asyncsleep(1000); // wait a bit
  try {
    raw_index_ptr.value = JSON.parse(raw_jsons.value[variant].join(""));
  } catch (error) {
    index_state.value = [variant == "compact" ? "cError" : "eError"];
    console.error("Error parsing concatenated JSON:", error);
  }

  /* Fill circle index */
  index_ptr.value = recursive_fill_circle_indexes(
    raw_index_ptr.value,
    [],
    variant
  );

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
  try {
    return new RegExp(keywords.value, "i"); // 'i' for case-insensitive
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

    if (use_regex.value && query.length > 0) {
      if (!regex_expr.value) {
        // Invalid regex
        return false;
      }
      return (
        circle_lowered.names.some((name) => regex_expr.value.test(name)) || // Check if any name in the circle's names array matches the regex
        regex_expr.value.test(circle_lowered.event_name) || // Check for event match
        (circle_lowered.misc &&
          circle_lowered.misc.some((misc) => regex_expr.value.test(misc)))
      );
    } else {
      return (
        circle_lowered.names.some((name) => name.includes(query)) || // Check if any name in the circle's names array includes the search query
        circle_lowered.event_name.toLowerCase().includes(query) || // Check for event match
        (circle_lowered.misc &&
          circle_lowered.misc.some((misc) =>
            misc.toLowerCase().includes(query)
          ))
      );
    }
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
    return `"${String(v).replace(/"/g, '""').replace(/\t/g, "\\t").replace(/\r?\n/g, "\\n")}"`;
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
    Successfully loaded circle index metadata.
  </div>
  <div v-if="index_state[0] == 'cLoading'" class="status-message">
    Loading Compact Circle Index... Downloaded {{ index_state[1] }} /
    {{ metadata?.compact_index_chunk_count }}...
  </div>
  <div v-if="index_state[0] == 'cParsing'" class="status-message">
    Parsing Compact Circle Index...
  </div>
  <div v-if="index_state[0] == 'cLoaded'" class="status-message">
    Successfully loaded Compact Circle Index.
  </div>
  <div v-if="index_state[0] == 'eLoading'" class="status-message">
    Loading Extensive Circle Index... Downloaded {{ index_state[1] }} /
    {{ metadata?.extensive_index_chunk_count }}...
  </div>
  <div v-if="index_state[0] == 'eParsing'" class="status-message">
    Parsing Extensive Circle Index...
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
  <div v-if="index_state[0] == 'Loaded'" class="status-message">
    <button
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
  </div>
  <div
    v-if="index_state[0] == 'Loaded' || index_state[0] == 'cLoaded'"
    class="status-message"
  >
    <button
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

  <input
    class="cp-input"
    :value="keywords"
    @input="onSearchUpdate"
    placeholder="Keywords"
  />
  <ToggleSwitch
    v-model:toggle_value="use_regex"
    :titleFunc="
      (state) => (state ? 'regex search enabled' : 'regex search disabled')
    "
  />
  ({{ filtered_circles?.length }} results)

  <!-- Align right -->
  <button
    class="ds-button"
    @click="dumpFilteredCircles()"
    title="Dump search results to csv."
    style="float: right; margin-right: 1.5em"
  >
    Dump search results
  </button>

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
              <!== {{ circle }} ==>
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
  background-color: var(--grey-dark);
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
