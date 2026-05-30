<script setup>
import { asyncsleep, PATH_DB_EXPORTED, fetch_url } from "@/assets/utils.js";
import { computed, ref, useTemplateRef, onMounted, markRaw  } from "vue";
import PopUpManager from "@/components/PopUpManager.vue";
import PopUpCirclePartialdetails from "./PopUpCirclePartialdetails.vue";
import axiosInstance from "@/axios/axios_config.js";
import SearchableVirtualList from "@/components/SearchableVirtualList.vue";

const debounce_ms = 180;
const metadata = ref({});
const circle_compact_index_parts = ref([]);
const circle_extensive_index_parts = ref([]);
const circle_compact_index = ref([]);
const circle_extensive_index = ref([]);
const index_state = ref({
  stage: "Idle",
  fetched: 0,
  parsed: 0,
});

/* Fetch circle index metadata */
async function fetch_metadata() {
  fetch_url({
    url: [PATH_DB_EXPORTED].concat([`circle_index_metadata.json`]).join("/"),
    axiosInstance: axiosInstance,
    on_start: () => {
      metadata.value = {};
      index_state.value = { stage: "Loading", fetched: 0, parsed: 0 };
    },
    on_success: (fetched_data) => {
      metadata.value = fetched_data;
      index_state.value = { stage: "Loaded", fetched: 0, parsed: 0 };
    },
    on_error: () => {
      index_state.value = { stage: "Error", fetched: 0, parsed: 0 };
    },
  });
}

/* Fetch circle raw indexes */
async function fetch_circle_raw_indexes(variant, batch_size = 5) {
  let base_url = "";
  let index_count = 0;
  let index_parts_ptr = null;
  let index_ptr = null;
  let loading_state = "";
  let loading_parsing_state = "";
  let parsing_state = "";
  let loaded_state = "";
  let error_state = "";
  if (variant == "compact") {
    index_parts_ptr = circle_compact_index_parts;
    index_ptr = circle_compact_index;
    base_url = [PATH_DB_EXPORTED]
      .concat(["circle_participation_compact_index"])
      .join("/");
    index_count = metadata.value?.compact_index_chunk_count || 0;
    loading_state = "cLoading";
    loading_parsing_state = "cLoadingParsing";
    parsing_state = "cParsing";
    loaded_state = "cLoaded";
    error_state = "cError";
    index_state.value = { stage: loading_state, fetched: 0, parsed: 0 };
  } else if (variant == "extensive") {
    index_parts_ptr = circle_extensive_index_parts;
    index_ptr = circle_extensive_index;
    base_url = [PATH_DB_EXPORTED]
      .concat(["circle_participation_extensive_index"])
      .join("/");
    index_count = metadata.value?.extensive_index_chunk_count || 0;
    loading_state = "eLoading";
    loading_parsing_state = "eLoadingParsing";
    parsing_state = "eParsing";
    loaded_state = "eLoaded";
    error_state = "eError";
    index_state.value = { stage: loading_state, fetched: 0, parsed: 0 };
  } else {
    console.error("fetch_circle_raw_indexes: Unknown variant", variant);
    return;
  }

  // Preserve already-downloaded parts so we can resume without refetching.
  index_parts_ptr.value = index_parts_ptr.value || [];
  if (index_parts_ptr.value.length > 0) {
    console.log(
      `Resuming from ${index_parts_ptr.value.length} / ${index_count} for ${variant} index.`
    );
  }

  // Keep previously parsed entries as well; don't clear `index_ptr` when resuming.
  index_ptr.value = index_ptr.value || [];
  const inflight = new Map();
  // Track already downloaded part indices to avoid re-downloading them.
  const downloadedSet = new Set(index_parts_ptr.value);
  let next_fetch = 0;
  let downloaded_count = downloadedSet.size;
  let parsed_count = downloadedSet.size;
  let parsing_started = false;
  let aborted = false;

  const update_progress = () => {
    if (aborted) return;
    const stage = parsing_started
      ? downloaded_count < index_count
        ? loading_parsing_state
        : parsing_state
      : loading_state;
    index_state.value = {
      stage,
      fetched: downloaded_count,
      parsed: parsed_count,
    };
  };

  const launch_fetch = (index) => {
    const part_url = `${base_url}_${index}.json`;
    const promise = axiosInstance
      .get(part_url, { responseType: "json" })
      .then((response) => ({ ok: true, data: response.data }))
      .catch((error) => ({ ok: false, error }));

    inflight.set(index, promise);
    promise.then((result) => {
      if (result.ok) {
        // We'll increment downloaded_count when we process the result below.
        update_progress();
      }
    });
  };

  // Launch an initial batch, skipping parts already downloaded.
  while (next_fetch < index_count && inflight.size < batch_size) {
    if (downloadedSet.has(next_fetch)) {
      next_fetch += 1;
      continue;
    }
    launch_fetch(next_fetch);
    next_fetch += 1;
  }

  for (let i = 0; i < index_count; i++) {
    // Skip parts that were already downloaded and parsed previously.
    if (downloadedSet.has(i)) {
      continue;
    }

    if (!inflight.has(i)) {
      // Aborted
      launch_fetch(i);
    }

    const result = await inflight.get(i);
    inflight.delete(i);

    if (!result || !result.ok) {
      aborted = true;
      index_state.value = {
        stage: error_state,
        fetched: downloaded_count,
        parsed: parsed_count,
      };
      console.error("Error fetching data:", result?.error);
      return;
    }

    if (!parsing_started) {
      parsing_started = true;
      update_progress();
      await asyncsleep(10);
    }

    let parsed_chunk = [];
    try {
      parsed_chunk = recursive_fill_circle_indexes(result.data, [], variant);
    } catch (e) {
      aborted = true;
      index_state.value = {
        stage: error_state,
        fetched: downloaded_count,
        parsed: parsed_count,
      };
      console.error("Error parsing data:", e);
      return;
    }

    index_ptr.value = index_ptr.value.concat(parsed_chunk);

    // Mark this part as downloaded and parsed so future runs will skip it.
    if (!downloadedSet.has(i)) {
      index_parts_ptr.value.push(i);
      downloadedSet.add(i);
      downloaded_count += 1;
      parsed_count += 1;
    }

    update_progress();

    // Fill more inflight slots if available, skipping already downloaded parts.
    while (next_fetch < index_count && inflight.size < batch_size) {
      if (downloadedSet.has(next_fetch)) {
        next_fetch += 1;
        continue;
      }
      launch_fetch(next_fetch);
      next_fetch += 1;
    }
  }

  index_state.value = {
    stage: loaded_state,
    fetched: downloaded_count,
    parsed: parsed_count,
  };
}

function recursive_fill_circle_indexes(
  raw_index,
  ar_path = [],
  variant = "compact"
) {
  let current_circle_list = [];
  // Defensive: if raw_index is null or not an object, abort parsing.
  if (raw_index === null || typeof raw_index !== "object") {
    throw new Error("Invalid index node (expected object)");
  }

  // If raw_index is an array at this level, it's unexpected (no event name key).
  if (Array.isArray(raw_index)) {
    throw new Error("Invalid index node (unexpected array)");
  }

  for (const key in raw_index) {
    if (Array.isArray(raw_index[key])) {
      let event_circles = [];

      event_ar_paths.value[key] = ar_path.concat(key);
      for (const circle_i in raw_index[key]) {
        const raw_circle = raw_index[key][circle_i];
        const circle_to_add =
          variant == "extensive" ? raw_circle : { names: raw_circle };
        circle_to_add["event_name"] = key;
        event_circles.push(circle_to_add);
      }

      current_circle_list = [].concat(current_circle_list, event_circles);
    } else {
      const raw = recursive_fill_circle_indexes(
        raw_index[key],
        ar_path.concat(key),
        variant
      );
      current_circle_list = [].concat(current_circle_list, raw);
    }
  }

  return current_circle_list;
}

const circle_index = computed(() => {
  if (
    index_state.value.stage === "cLoaded" &&
    circle_compact_index &&
    circle_compact_index.value &&
    Array.isArray(circle_compact_index.value)
  ) {
    return circle_compact_index.value;
  } else if (
    index_state.value.stage === "eLoaded" &&
    circle_extensive_index &&
    circle_extensive_index.value &&
    Array.isArray(circle_extensive_index.value)
  ) {
    return circle_extensive_index.value;
  } else {
    return [];
  }
});

const event_ar_paths = ref({});

function circleSearchText(circle) {
  const toText = (value) => {
    if (Array.isArray(value)) {
      return value
        .map((entry) =>
          entry === null || entry === undefined ? "" : String(entry).trim()
        )
        .filter(Boolean)
        .join(" / ");
    }
    if (value === null || value === undefined) return "";
    return String(value).trim();
  };

  return [circle.event_name, toText(circle.names), toText(circle.misc)]
    .filter(Boolean)
    .join("\t");
}

/* PopUpManager */
const popUpManager = useTemplateRef("popUpManager");
function getEventHref(event_name) {
  const path = event_ar_paths.value[event_name] || [];
  return ["/dea/event_detail/#"].concat(path).join("/");
}

function popupCircleDetails(circle_partial_db) {
  popUpManager.value.addPopup(markRaw(PopUpCirclePartialdetails), {
    circle_db: circle_partial_db,
    db_path: event_ar_paths.value[circle_partial_db.event_name],
  });
}

onMounted(async () => {
  await fetch_metadata();
});
</script>

<template>
  <!-- Title -->
  <head>
    <title v-if="index_state.stage == 'eEnabled'">
      dea | Circle Participation (extensive search)
    </title>
    <title v-else>dea | Circle Participation</title>
  </head>

  <div class="header-title">Circle Participation</div>
  <div class="header">List of participating circles in the database.</div>

  <div v-if="index_state.stage == 'Loading'" class="status-message">
    Loading circle index metadata...
  </div>
  <div v-else-if="index_state.stage == 'Loaded'" class="status-message">
    Successfully loaded circle index metadata. One of the circle indexes can now
    be downloaded.
  </div>
  <div v-if="index_state.stage == 'cLoading'" class="status-message">
    Loading Compact Circle Index... Downloaded {{ index_state.fetched }} /
    {{ metadata?.compact_index_chunk_count }}...
  </div>
  <div v-if="index_state.stage == 'cLoadingParsing'" class="status-message">
    Loading Compact Circle Index... Downloaded {{ index_state.fetched }} /
    {{ metadata?.compact_index_chunk_count }}. Parsed {{ index_state.parsed }} /
    {{ metadata?.compact_index_chunk_count }}...
  </div>
  <div v-if="index_state.stage == 'cParsing'" class="status-message">
    Parsing Compact Circle Index... Parsed {{ index_state.parsed }} /
    {{ metadata?.compact_index_chunk_count }}...
  </div>
  <div v-if="index_state.stage == 'cLoaded'" class="status-message">
    Successfully loaded Compact Circle Index.
  </div>
  <div v-if="index_state.stage == 'eLoading'" class="status-message">
    Loading Extensive Circle Index... Downloaded {{ index_state.fetched }} /
    {{ metadata?.extensive_index_chunk_count }}...
  </div>
  <div v-if="index_state.stage == 'eLoadingParsing'" class="status-message">
    Loading Extensive Circle Index... Downloaded {{ index_state.fetched }} /
    {{ metadata?.extensive_index_chunk_count }}. Parsed {{ index_state.parsed }} /
    {{ metadata?.extensive_index_chunk_count }}...
  </div>
  <div v-if="index_state.stage == 'eParsing'" class="status-message">
    Parsing Extensive Circle Index... Parsed {{ index_state.parsed }} /
    {{ metadata?.extensive_index_chunk_count }}...
  </div>
  <div v-if="index_state.stage == 'eLoaded'" class="status-message">
    Successfully loaded Extensive Circle Index.
  </div>
  <div v-else-if="index_state.stage.endsWith('Error')" class="status-message">
    <!-- buttons -->
    Failed to fetch
    {{
      index_state.stage == "cError"
        ? "circle compact index"
        : index_state.stage == "eError"
        ? "circle extensive index"
        : "circle index metadata"
    }}.
    <button
      class="retry-button"
      @click="
        index_state.stage == 'Error'
          ? fetch_metadata()
          : index_state.stage == 'cError'
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
        v-if="index_state.stage == 'Loaded'"
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
        v-if="index_state.stage == 'Loaded' || index_state.stage == 'cLoaded'"
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
    <SearchableVirtualList
      class="cp-vlist"
      contour-color="var(--orange-dark)"
      rows-color="var(--grey-dark)"
      :items="circle_index"
      :search-text-getter="circleSearchText"
      :item-height="22"
      :debounce-ms="debounce_ms"
    >
      <template #header>
        <table class="cp-header-table">
          <thead>
            <tr>
              <th colspan="2" class="cp-table-title">Participating circles</th>
            </tr>
            <tr>
              <th>Names / Pen Names</th>
              <th>Event</th>
            </tr>
          </thead>
        </table>
      </template>

      <template #default="{ list }">
        <div
          v-for="vitem in list"
          :key="vitem.index"
          v-bind="vitem.rowProps"
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
                :href="getEventHref(vitem.data.event_name)"
              >
                {{ vitem.data.event_name }}
              </a>
            </div>
          </div>
        </div>
      </template>
    </SearchableVirtualList>
  </div>
  <PopUpManager ref="popUpManager" />
</template>

<style scoped>
@import "@/assets/common.css";

/* Container and header */
.cp-div {
  margin: 1em;
  color: var(--grey-vibrant);
  text-align: left;
  font-size: 18px;
  font-family: Arial, sans-serif;
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
  height: 66vh;
  max-height: 66vh;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

/* The vlist container must be the scroll container. Keep a single definition. */
.cp-vlist-component {
  flex: 1 1 auto;
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
.cp-body-table {
  table-layout: fixed;
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
}
.cp-body-table td,
.cp-body-table th {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding: 0 0.3em;
  line-height: 22px;
  height: 22px;
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
  padding: 0;
  height: var(--svl-item-height);
  line-height: var(--svl-item-height);
  display: inline-flex;
  align-items: center;
  justify-content: center;
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
