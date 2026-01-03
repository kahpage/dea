<!--============================================================ ...
     Check page
... ============================================================ -->

<script setup>
import Navigation from "@/components/Navigation.vue";
import axiosInstance from "@/axios/axios_config.js";
import { computed, onMounted, ref, watch, reactive } from "vue";
import ToggleShow from "@/components/ToggleShow.vue";
import BarChart from "@/components/BarChart.vue";

import {
  PATH_DB_EXPORTED,
  PATH_DB_TO_EXPORT,
  fetch_url,
  isImage,
} from "@/assets/utils.js";

const verify_db = ref({}); // {eg: {...events}}
const verify_db_state = ref("loading"); // 'loading', 'loaded', 'error'

async function fetch_verify_db() {
  fetch_url({
    url: [PATH_DB_EXPORTED].concat("verify_index.json").join("/"),
    axiosInstance: axiosInstance,
    on_start: () => {
      verify_db.value = {};
      verify_db_state.value = "loading";
    },
    on_success: (fetched_data) => {
      verify_db.value = fetched_data;
      verify_db_state.value = "loaded";
    },
    on_error: (error) => {
      verify_db_state.value = "error";
    },
  });
}

function recursive_flaten_verify_db(verify_index, ar_path = []) {
  let event_groups_list = []; // Array of {key, name, ar_path, events}

  let subcategs = Object.keys(verify_index).filter(
    (k) => k !== "@databases" && k !== "@count"
  );
  subcategs.sort((a, b) => a.localeCompare(b));

  let event_groups_raw = verify_index["@databases"] || {};

  // Sort event groups deterministically by their display name (alias) or key
  const event_group_entries = Object.entries(event_groups_raw).sort(
    ([, a], [, b]) => {
      const nameA = (a && a.key) || "";
      const nameB = (b && b.key) || "";
      return nameA.localeCompare(nameB);
    }
  );

  // == Collect event groups (without hue assignment) ==
  for (const [event_group_key, event_group] of event_group_entries) {
    let event_group_ar_path = ar_path.concat([event_group_key]);
    let pathStr = event_group_ar_path.join("/");

    // add ar_path to event group object
    event_group.ar_path = event_group_ar_path;

    event_groups_list.push(event_group);
  }

  // == Sub categories ==
  for (const key of subcategs) {
    const sub_groups = recursive_flaten_verify_db(
      verify_db.value[key],
      ar_path.concat([key])
    );
    event_groups_list = event_groups_list.concat(sub_groups);
  }

  return event_groups_list;
}

const flat_verify_db = computed(() => {
  return recursive_flaten_verify_db(verify_db.value);
});

const all_event_groups = computed(() => {
  const groups = flat_verify_db.value;
  const total = groups.length;
  return groups.map((group, index) => {
    const pathStr = group.ar_path ? group.ar_path.join("/") : "";
    return {
      ...group,
      pathStr: pathStr,
      link: "/dea/event_group_detail/#/" + pathStr,
      hue: total > 0 ? (360 * index) / total : 0,
    };
  });
});

// Visibility state for event groups (keyed by group.pathStr)
const visibleGroups = ref({});

watch(
  all_event_groups,
  (groups) => {
    if (!groups) return;
    // Initialize visibility to true for new groups, preserve existing toggles
    for (const g of groups) {
      if (!(g.pathStr in visibleGroups.value)) {
        visibleGroups.value[g.pathStr] = true;
      }
    }
  },
  { immediate: true }
);

function setAllGroupsVisible(visible) {
  const groups = all_event_groups.value || [];
  for (const g of groups) {
    visibleGroups.value[g.pathStr] = visible;
  }
}

function selectAllGroups() {
  setAllGroupsVisible(true);
}
function selectNoneGroups() {
  setAllGroupsVisible(false);
}

const legendItems = computed(() => {
  return all_event_groups.value.map((group) => ({
    name: group.name,
    hue: group.hue,
    link: group.link,
    pathStr: group.pathStr,
  }));
});

const filtered_verify_db = computed(() => {
  return all_event_groups.value.filter((g) => visibleGroups.value[g.pathStr]);
});

const dummy = computed(() => {
  console.log("Flattened verify list:", verify_db.value);
  return flat_verify_db.value;
});

const shownEventsCount = computed(() => {
  return filtered_verify_db.value.length;
});

function getMaxMediaCount(eg) {
  if (!eg || !eg.events) return 0;
  const counts = Object.values(eg.events).map((e) =>
    e.media ? e.media.length : 0
  );
  // include group-level media defined at eg.media
  counts.push(eg.media ? eg.media.length : 0);
  return Math.max(0, ...counts);
}

// Track media load failures keyed by "eg.pathStr::eventName::index"
const failedMedia = reactive({});
function markMediaFailed(key) {
  failedMedia[key] = true;
}
function mediaFailed(key) {
  return !!failedMedia[key];
}

// Helper to safely extract a displayable basename from a media entry
function mediaBasename(item) {
  if (typeof item === "string") return item.split("/").pop();
  if (!item && item !== 0) return "";
  if (Array.isArray(item)) return item.map(String).join("/");
  if (typeof item === "object") {
    if (item.name) return String(item.name);
    try {
      return JSON.stringify(item);
    } catch (e) {
      return String(item);
    }
  }
  return String(item);
}

// Helper to produce a readable label for non-string media entries
function mediaLabel(item) {
  if (typeof item === "string") return item;
  if (!item && item !== 0) return "";
  if (typeof item === "object") {
    try {
      return JSON.stringify(item);
    } catch (e) {
      return String(item);
    }
  }
  return String(item);
}

// Count failed media for a given key prefix. If `type` === 'group' it checks eg.media, otherwise checks eg.events[eventName].media
function getMediaErrorCount(eg, eventName = null) {
  let count = 0;
  if (eventName === null) {
    // group-level
    if (!eg.media) return 0;
    for (let idx = 0; idx < eg.media.length; idx++) {
      if (failedMedia[eg.pathStr + "::group::" + idx]) count++;
    }
    return count;
  }
  // per-event
  const ev = eg.events && eg.events[eventName];
  if (!ev || !ev.media) return 0;
  for (let idx = 0; idx < ev.media.length; idx++) {
    if (failedMedia[eg.pathStr + "::" + eventName + "::" + idx]) count++;
  }
  return count;
}
// Get total error count for entire group (group media + all events)
function getTotalGroupErrors(eg) {
  let total = getMediaErrorCount(eg); // group-level errors
  if (eg.events) {
    Object.keys(eg.events).forEach(eventName => {
      total += getMediaErrorCount(eg, eventName);
    });
  }
  return total;
}

// Preload all group-level images to trigger error detection
function preloadGroupMedia(eg) {
  // Preload group-level media
  if (eg.media && eg.media.length > 0) {
    eg.media.forEach((item, idx) => {
      const path = typeof item === 'string' ? item : item?.path;
      if (!path || !isImage(path)) return;
      
      const imgUrl = PATH_DB_TO_EXPORT + '/' + eg.ar_path.concat(['media']).join('/') + '/' + path;
      const img = new Image();
      img.onload = () => {
        // Successfully loaded, nothing to do
      };
      img.onerror = () => {
        markMediaFailed(eg.pathStr + '::group::' + idx);
      };
      img.src = imgUrl;
    });
  }

  // Preload all event-level media
  if (eg.events) {
    Object.keys(eg.events).forEach(eventName => {
      const event = eg.events[eventName];
      if (!event.media || event.media.length === 0) return;
      
      event.media.forEach((item, idx) => {
        const path = typeof item === 'string' ? item : item?.path;
        if (!path || !isImage(path)) return;
        
        const imgUrl = PATH_DB_TO_EXPORT + '/' + eg.ar_path.concat(['media']).join('/') + '/' + path;
        const img = new Image();
        img.onload = () => {
          // Successfully loaded, nothing to do
        };
        img.onerror = () => {
          markMediaFailed(eg.pathStr + '::' + eventName + '::' + idx);
        };
        img.src = imgUrl;
      });
    });
  }
}
/* Run fetch_verify_db on component mount */
onMounted(async () => {
  await fetch_verify_db();
});
</script>

<template>
  <!-- Title -->
  <head>
    <title>dea | Verify</title>
  </head>

  <div class="vf-container">
    <div class="vf-content">
      <section id="top"></section>
      <Navigation />
      <div class="header-title">Verify</div>
      <div class="header">
        Various tools for database verification and visualization.
      </div>

      <div class="status-message" v-if="verify_db_state === 'loading'">
        Fetching verify db...
      </div>
      <div class="status-message" v-else-if="verify_db_state === 'error'">
        Failed to fetch verify db.
        <button
          class="retry-button"
          @click="fetch_verify_db"
          title="Retry fetching verify db."
        >
          Retry
        </button>
      </div>
      <div v-else>
        <!-- Successfully fetched verify db-->
        <!-- Legend -->
        <div class="legend-container">
          <div
            v-for="item in legendItems"
            :key="item.pathStr"
            class="legend-item"
          >
            <input
              type="checkbox"
              :id="'legend-' + item.pathStr"
              v-model="visibleGroups[item.pathStr]"
              class="legend-checkbox"
              :style="{
                backgroundColor: visibleGroups[item.pathStr]
                  ? `hsl(${item.hue}, var(--event-active-saturation), var(--event-lightness))`
                  : 'transparent',
                borderColor: `hsl(${item.hue}, var(--event-active-saturation), var(--event-lightness))`,
              }"
              title="Toggle visibility"
            />
            <a :href="item.link" class="legend-text">{{ item.name }}</a>
          </div>
        </div>

        <div
          style="
            display: flex;
            gap: 0.75em;
            align-items: center;
            justify-content: center;
            margin-top: 0.5em;
          "
        >
          <button class="retry-button" @click="selectAllGroups">
            Show all
          </button>
          <button class="retry-button" @click="selectNoneGroups">
            Show none
          </button>
          <span
            style="
              color: var(--grey-mild);
              font-size: 0.95em;
              margin-left: 0.5em;
            "
          >
            Showing {{ shownEventsCount }} groups
          </span>
        </div>

        <!-- Verification tools -->
        <!-- Circle participation bar charts -->
        <ToggleShow
          class="vf-toggle-show"
          :button_text="'Circle Participation Charts'"
        >
          <div
            class="vf-eg-div"
            v-for="eg in filtered_verify_db"
            :key="eg.name"
          >
            <div class="vf-eg-name-container">
              <a :href="eg.link" class="vf-eg-name">{{ eg.name }}</a>
            </div>
            <div class="vf-eg-content">
              <p v-if="!eg.events" class="status-message">
                No events in this event group.
              </p>
              <BarChart
                v-else
                :data="
                  Object.keys(eg.events).map((e) => ({
                    value: eg.events[e].circle_count,
                    name: e,
                    prefix: eg.events[e]?.dates,
                    url: ['/dea/event_detail/#']
                      .concat(eg.ar_path || [])
                      .concat([e])
                      .join('/'),
                  }))
                "
                :title="'Event participation'"
              />
            </div>
          </div>
        </ToggleShow>
        <br />

        <!-- Media -->
        <ToggleShow class="vf-toggle-show" :button_text="'Media'">
          <div
            class="vf-eg-div"
            v-for="eg in filtered_verify_db"
            :key="eg.name"
          >
            <div class="vf-eg-name-container">
              <a :href="eg.link" class="vf-eg-name">{{ eg.name }}</a>
              <button
                class="preload-button-vertical"
                @click="preloadGroupMedia(eg)"
                title="Preload all images of the event group"
              >⟳</button>
              <span 
                class="error-count-vertical"
                v-if="getTotalGroupErrors(eg) > 0"
                :title="getTotalGroupErrors(eg) + (getTotalGroupErrors(eg) === 1 ? ' total error' : ' total errors')"
              >({{ getTotalGroupErrors(eg) }})</span>
            </div>
            <div class="vf-eg-content">
              <p v-if="!eg.events" class="error-text">
                No events in this event group.
              </p>
              <div v-else class="media-container">
                <table class="media-table">
                  <thead>
                    <tr>
                      <th key="group-header">
                        Event Group
                        <span
                          class="header-error-count"
                          v-if="getMediaErrorCount(eg) > 0"
                          :title="
                            getMediaErrorCount(eg) +
                            (getMediaErrorCount(eg) === 1
                              ? ' media loading error'
                              : ' media loading errors')
                          "
                          >({{ getMediaErrorCount(eg) }})</span
                        >
                      </th>
                      <th
                        v-for="eventName in Object.keys(eg.events)"
                        :key="eventName"
                      >
                        <a
                          :href="
                            ['/dea/event_detail/#']
                              .concat(eg.ar_path || [])
                              .concat([eventName])
                              .join('/')
                          "
                        >
                          {{ eventName }}
                        </a>
                        <span
                          class="header-error-count"
                          v-if="getMediaErrorCount(eg, eventName) > 0"
                          :title="
                            getMediaErrorCount(eg, eventName) +
                            (getMediaErrorCount(eg, eventName) === 1
                              ? ' media loading error'
                              : ' media loading errors')
                          "
                          >({{ getMediaErrorCount(eg, eventName) }})</span
                        >
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="i in getMaxMediaCount(eg)" :key="i">
                      <!-- group-level media column -->
                      <td
                        :key="'group-' + i"
                        :class="{
                          'empty-cell': !eg.media || !eg.media[i - 1],
                        }"
                      >
                        <div
                          v-if="eg.media && eg.media[i - 1]"
                          class="media-item"
                        >
                          <div v-if="isImage(eg.media[i - 1])">
                            <div
                              v-if="
                                !mediaFailed(eg.pathStr + '::group::' + (i - 1))
                              "
                            >
                              <img
                                :src="
                                  PATH_DB_TO_EXPORT +
                                  '/' +
                                  eg.ar_path.concat(['media']).join('/') +
                                  '/' +
                                  eg.media[i - 1]
                                "
                                class="media-image"
                                loading="lazy"
                                @error="
                                  markMediaFailed(
                                    eg.pathStr + '::group::' + (i - 1)
                                  )
                                "
                                :title="mediaBasename(eg.media[i - 1])"
                              />
                            </div>
                            <div
                              v-else
                              class="error-text"
                              :title="mediaBasename(eg.media[i - 1])"
                            >
                              LOADING ERROR
                            </div>
                            {{ mediaLabel(eg.media[i - 1]) }}
                          </div>
                          <div v-else>
                            <a
                              :href="
                                PATH_DB_TO_EXPORT +
                                '/' +
                                eg.ar_path.concat(['media']).join('/') +
                                '/' +
                                eg.media[i - 1]
                              "
                              target="_blank"
                              :title="mediaBasename(eg.media[i - 1])"
                              >{{ eg.media[i - 1] }}</a
                            >
                          </div>
                        </div>
                      </td>

                      <!-- per-event media columns -->
                      <td
                        v-for="eventName in Object.keys(eg.events)"
                        :key="eventName"
                        :class="{
                          'empty-cell':
                            !eg.events[eventName].media ||
                            !eg.events[eventName].media[i - 1],
                        }"
                      >
                        <div
                          v-if="
                            eg.events[eventName].media &&
                            eg.events[eventName].media[i - 1]
                          "
                          class="media-item"
                        >
                          <div
                            v-if="isImage(eg.events[eventName].media[i - 1])"
                          >
                            <div
                              v-if="
                                !mediaFailed(
                                  eg.pathStr + '::' + eventName + '::' + (i - 1)
                                )
                              "
                            >
                              <img
                                :src="
                                  PATH_DB_TO_EXPORT +
                                  '/' +
                                  eg.ar_path.concat(['media']).join('/') +
                                  '/' +
                                  eg.events[eventName].media[i - 1]
                                "
                                class="media-image"
                                loading="lazy"
                                @error="
                                  markMediaFailed(
                                    eg.pathStr +
                                      '::' +
                                      eventName +
                                      '::' +
                                      (i - 1)
                                  )
                                "
                                :title="
                                  mediaBasename(
                                    eg.events[eventName].media[i - 1]
                                  )
                                "
                              />
                            </div>
                            <div
                              v-else
                              class="error-text"
                              :title="
                                mediaBasename(eg.events[eventName].media[i - 1])
                              "
                            >
                              LOADING ERROR
                            </div>
                            {{ mediaLabel(eg.events[eventName].media[i - 1]) }}
                          </div>
                          <div v-else>
                            <a
                              :href="
                                PATH_DB_TO_EXPORT +
                                '/' +
                                eg.ar_path.concat(['media']).join('/') +
                                '/' +
                                eg.events[eventName].media[i - 1]
                              "
                              target="_blank"
                              :title="
                                mediaBasename(eg.events[eventName].media[i - 1])
                              "
                              >{{
                                mediaLabel(eg.events[eventName].media[i - 1])
                              }}</a
                            >
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </ToggleShow>
        <br />
      </div>

      <!-- <div v-for="eg in filtered_verify_db" :key="eg.name">
        {{ eg.name }} : {{ eg }}
      </div> -->
      <!-- dummy={{ dummy }} -->
    </div>
  </div>
</template>

<style>
@import "@/assets/common.css";

.vf-container {
  display: flex;
  flex-direction: row;
  height: 100vh;
  width: 100%;
}

.vf-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden; /* prevent page-level horizontal overflow from inner panels */
  padding: 0;
  box-sizing: border-box;
}

.vf-menu {
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

.legend-checkbox {
  width: 1.6em;
  height: 1.6em;
  border-radius: 50%;
  -webkit-appearance: none;
  appearance: none;
  border: 2px solid rgba(0, 0, 0, 0.12);
  display: inline-block;
  vertical-align: middle;
  cursor: pointer;
  box-sizing: border-box;
  transition: background-color 120ms ease, transform 80ms ease,
    box-shadow 120ms ease, border-color 120ms ease;
}

.legend-checkbox:focus {
  outline: none;
  box-shadow: 0 0 0 0.15em rgba(0, 0, 0, 0.08);
}

.legend-checkbox:not(:checked) {
  background-color: transparent !important;
}

.legend-checkbox:checked {
  transform: scale(0.96);
  box-shadow: inset 0 0 0 2px rgba(0, 0, 0, 0.15);
}

.legend-text {
  color: var(--grey-mild);
  font-size: 0.9em;
}

.vf-eg-div {
  display: flex;
  flex-direction: row;
  border: 2px solid var(--green-mild);
  border-radius: 0.5em;
  margin-bottom: 1em;
  background-color: white;
  min-height: 100px;
  box-sizing: border-box;
  overflow: hidden; /* hide any accidental overflow from children */
}

.vf-eg-name-container {
  background-color: var(--green-mild);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  padding: 0.5em;
  border-top-right-radius: 0.2em;
  border-bottom-right-radius: 0.2em;
  min-width: 2.5em;
}

.vf-eg-name {
  color: var(--grey-vibrant);
  writing-mode: vertical-rl;
  text-orientation: sideways;
  transform: rotate(180deg);
  text-align: center;
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  background-color: transparent;
  text-decoration: none;
}

.preload-button-vertical {
  background-color: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.5);
  color: var(--grey-vibrant);
  font-size: 1.2em;
  padding: 0em;
  border-radius: 0.3em;
  cursor: pointer;
  transition: background-color 0.15s ease;
  min-width: 1em;
  min-height: 1em;
  max-width: 1em;
  max-height: 1em;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preload-button-vertical:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

.preload-button-vertical:active {
  background-color: rgba(255, 255, 255, 0.2);
}

.error-count-vertical {
  color: #ff5b5b;
  font-weight: 700;
  font-size: 0.95em;
  /* background-color: rgba(255, 255, 255, 0.9); */
  padding: 0.25em 0.5em;
  border-radius: 0.3em;
}

.vf-eg-content {
  color: var(--grey-vibrant);
  background-color: var(--greyish-dark);
  flex: 1;
  padding: 0.5em;
  box-sizing: border-box;
  min-width: 0; /* allow flex child to shrink to prevent overflow */
  overflow-x: auto; /* horizontal scroll for large content */
  overflow-y: hidden;
}

.vf-eg-content img,
.vf-eg-content pre,
.vf-eg-content table {
  max-width: 100%;
  box-sizing: border-box;
}

/* ToggleShow spacing */
.vf-toggle-show {
  margin-left: 0.5em;
  box-sizing: border-box;
  display: inline-block; /* allow it to shrink to the button when closed */
  vertical-align: top;
  width: auto; /* allow it to be smaller when content is small */
  max-width: calc(100% - 1em); /* cap width to leave 0.5em gap on both sides */
  padding-right: 0.5em; /* ensure a visible gap to the right edge */
}

/* ToggleShow root overrides */
.vf-toggle-show.ts-div {
  box-sizing: border-box !important;
  margin-left: 0.5em !important; /* restore left margin */
  margin-right: 0.5em !important; /* ensure right margin */
  max-width: calc(100% - 1em) !important; /* respect both side margins */
}

/* ToggleShow open: expand */
.vf-toggle-show.ts-open {
  display: block !important;
  width: calc(100% - 1em) !important;
  max-width: calc(100% - 1em) !important;
}

/* ToggleShow content: fill width */
.vf-toggle-show .ts-content {
  display: block;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.media-container {
  overflow-x: auto;
  overflow-y: auto;
  max-width: 100%;
  max-height: 60vh;
  position: relative;
}

.media-table {
  border-collapse: separate;
  border-spacing: 0;
  table-layout: fixed; /* enforce fixed column widths so cells respect min-width */
}

.media-table th,
.media-table td {
  border: 1px solid var(--grey-mild);
  padding: 0.5em;
  width: 10em;
  min-width: 10em;
  max-width: 10em;
  vertical-align: top;
  background-color: var(--greyish-light);
  overflow: hidden; /* keep contents inside cell */
  /* allow wrapping and breaking inside the fixed-width cell */
  overflow-wrap: anywhere;
  word-break: break-all; /* cut words if necessary */
  white-space: normal; /* allow multi-line wrapping */
}

.media-table th {
  background-color: var(--scarlet-soft);
  color: white;
  font-weight: bold;
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 2px solid var(--grey-dark);
}

.header-error-count {
  color: #ffa0a0;
  font-size: 0.85em;
  margin-left: 0.35em;
}

.preload-button {
  /* background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4); */
  color: white;
  font-size: 1em;
  padding: 0.2em 0.4em;
  border-radius: 0.3em;
  cursor: pointer;
  /* transition: background-color 0.15s ease; */
}

.preload-button:hover {
  background-color: rgba(255, 255, 255, 0.35);
}

.preload-button:active {
  background-color: rgba(255, 255, 255, 0.15);
}

.media-item {
  margin-bottom: 0.5em;
}

.media-image {
  width: 100%;
  height: auto;
  max-height: 10em;
  object-fit: contain;
}

/* ensure long links or filenames wrap or break inside cells */
.media-table td a {
  display: block;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.media-table td.empty-cell {
  background-color: var(--greyish-dark);
}

.error-text {
  color: #ffa0a0;
  font-weight: 700;
  font-size: 0.95em;
}
</style>
