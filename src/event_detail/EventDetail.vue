<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import { ref, computed, watchEffect } from "vue";
import { useVirtualList } from "@vueuse/core";
import axiosInstance from "@/axios/axios_config.js";
import {
  makeLinksClickable,
  PATH_DB_TO_EXPORT,
  PATH_DB_EXPORTED,
  fetch_url,
} from "@/assets/utils.js";
import ToggleShow from "@/components/ToggleShow.vue";
import ToggleSwitch from "@/components/ToggleSwitch.vue";
import { useTemplateRef, markRaw } from "vue";

import PopUpManager from "@/components/PopUpManager.vue";
import MediaGrid from "@/components/MediaGrid.vue";
import PopUpCircledetails from "./PopUpCircledetails.vue";

const props = defineProps({
  db_path: String,
});

const keywords = ref(""); // For filtering circles in the virtual list
const use_regex = ref(false); // Whether to use regex search or not

const regex_expr = computed(() => {
  try {
    return new RegExp(keywords.value, "i");
  } catch (e) {
    return null;
  }
});
const event_data = ref(null);
const event_data_state = ref("loading"); // 'loading', 'loaded', 'error'

async function fetch_ed_db() {
  fetch_url({
    url: [PATH_DB_EXPORTED].concat(db_path_args.value).join("/") + ".json",
    axiosInstance: axiosInstance,
    on_start: () => {
      event_data.value = {};
      event_data_state.value = "loading";
    },
    on_success: (fetched_data) => {
      if (!fetched_data.hasOwnProperty("aliases")) {
        throw new Error("Invalid data format: 'aliases' property missing");
      }
      event_data.value = fetched_data;
      event_data_state.value = "loaded";
    },
    on_error: (error) => {
      event_group_data_state.value = "error";
    },
  });
}

// Filtered circles based on keywords
const filtered_circles = computed(() => {
  if (!event_data.value || !event_data.value.circles) {
    return [];
  }
  // trim to treat whitespace-only as empty
  const rawKw = (keywords.value || "").trim();
  if (!rawKw) {
    return event_data.value.circles;
  }

  // If regex mode is enabled, use regex matching (case-insensitive)
  if (use_regex.value && rawKw.length > 0) {
    if (!regex_expr.value) return [];
    const re = regex_expr.value;
    return event_data.value.circles.filter((circle) => {
      const anyMatch = (arr) =>
        Array.isArray(arr) &&
        arr.some((s) => typeof s === "string" && re.test(s));

      if (anyMatch(circle.aliases)) return true;
      if (anyMatch(circle.pen_names)) return true;
      if (
        circle.position !== undefined &&
        circle.position !== null &&
        re.test(circle.position.toString())
      )
        return true;
      if (anyMatch(circle.links)) return true;

      return false;
    });
  }

  // Default substring matching (case-insensitive)
  const kw = rawKw.toLowerCase();
  return event_data.value.circles.filter((circle) => {
    const anyIncludes = (arr) =>
      Array.isArray(arr) &&
      arr.some((s) => typeof s === "string" && s.toLowerCase().includes(kw));

    if (anyIncludes(circle.aliases)) return true;
    if (anyIncludes(circle.pen_names)) return true;

    if (
      circle.position !== undefined &&
      circle.position !== null &&
      circle.position.toString().toLowerCase().includes(kw)
    )
      return true;

    if (anyIncludes(circle.links)) return true;

    return false;
  });
});

// Virtual list
function onSearchUpdate(event) {
  // Sync keywords with text input
  keywords.value = event.target.value;
  scrollTo(0);
}
const { list, containerProps, wrapperProps, scrollTo } = useVirtualList(
  filtered_circles,
  {
    // Fixed item height must match the CSS row height to avoid
    // virtualization rendering artifacts for large lists.
    itemHeight: 22,
    // overscan: 10,
  }
);

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
    if (props.db_path) {
      await fetch_ed_db();
    }
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
  <div class="status-message" v-if="event_data_state == 'loading'">
    Loading database {{ props.db_path }}...
  </div>
  <div class="status-message" v-else-if="event_data_state == 'error'">
    Failed to fetch event group data.
    <button
      class="retry-button"
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

      <!-- ===== CIRCLE LIST (virtualized) ===== -->

      <div
        v-if="event_data?.circles && Array.isArray(event_data.circles)"
        class="ed-div-table"
      >
        <div class="ed-search-row">
          <input
            class="ed-input"
            :value="keywords"
            @input="onSearchUpdate"
            placeholder="Keywords"
          />

          <div class="ed-input ed-regex-group">
            <div class="ed-regex-label">Use Regex ?</div>
            <ToggleSwitch
              v-model:toggle_value="use_regex"
              :titleFunc="
                (state) =>
                  state ? 'regex search enabled' : 'regex search disabled'
              "
            />
          </div>

          <div class="ed-results">({{ filtered_circles?.length }} results)</div>
        </div>
        <table class="ed-header-table">
          <thead>
            <tr>
              <th colspan="5" class="ed-table-title">Participating circles</th>
            </tr>
            <tr>
              <th style="width: 5%">Details</th>
              <th style="width: 10%">Position</th>
              <th style="width: 30%">Aliases</th>
              <th style="width: 25%">Pen Names</th>
              <th style="width: 30%">Links</th>
            </tr>
          </thead>
        </table>

        <div class="ed-vlist">
          <div v-bind="containerProps" class="ed-vlist-component">
            <div v-bind="wrapperProps" class="ed-vlist-wrapper">
              <table class="ed-body-table">
                <colgroup>
                  <col style="width: 5%" />
                  <col style="width: 10%" />
                  <col style="width: 30%" />
                  <col style="width: 25%" />
                  <col style="width: 30%" />
                </colgroup>
                <tbody>
                  <tr
                    v-for="vitem in list"
                    :key="vitem.index"
                    :class="[
                      'ed-vlist-item',
                      vitem.index % 2 === 0
                        ? 'ed-vlist-item-even'
                        : 'ed-vlist-item-odd',
                    ]"
                  >
                    <td
                      :style="{
                        backgroundColor:
                          vitem.index % 2 === 0
                            ? 'var(--grey-dark)'
                            : 'var(--greyish-deep)',
                        color: 'var(--grey-light)',
                        textAlign: 'center',
                      }"
                    >
                      <button
                        class="ed-popup-button"
                        @click="popupCircleDetails(vitem.data)"
                        title="Show circle details"
                      >
                        🡵
                      </button>
                    </td>
                    <td
                      :style="{
                        backgroundColor:
                          vitem.index % 2 === 0
                            ? 'var(--grey-dark)'
                            : 'var(--greyish-deep)',
                        color: 'var(--grey-light)',
                      }"
                    >
                      {{ vitem.data.position ?? "" }}
                    </td>
                    <td
                      :style="{
                        backgroundColor:
                          vitem.index % 2 === 0
                            ? 'var(--grey-dark)'
                            : 'var(--greyish-deep)',
                        color: 'var(--grey-light)',
                      }"
                    >
                      {{
                        Array.isArray(vitem.data.aliases)
                          ? vitem.data.aliases.join(" / ")
                          : vitem.data.aliases || ""
                      }}
                    </td>
                    <td
                      :style="{
                        backgroundColor:
                          vitem.index % 2 === 0
                            ? 'var(--grey-dark)'
                            : 'var(--greyish-deep)',
                        color: 'var(--grey-light)',
                      }"
                    >
                      {{
                        Array.isArray(vitem.data.pen_names)
                          ? vitem.data.pen_names.join(" / ")
                          : vitem.data.pen_names || ""
                      }}
                    </td>
                    <td
                      :style="{
                        backgroundColor:
                          vitem.index % 2 === 0
                            ? 'var(--grey-dark)'
                            : 'var(--greyish-deep)',
                        color: 'var(--grey-light)',
                      }"
                    >
                      <span
                        v-html="
                          makeLinksClickable(
                            Array.isArray(vitem.data.links)
                              ? vitem.data.links.join(', ')
                              : vitem.data.links || ''
                          )
                        "
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
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

      <!-- ===== Location ===== -->
      <ToggleShow
        class="ts-sources"
        :button_text="'Location'"
        v-if="event_data?.locations"
      >
        <div v-for="(loc, i) in event_data.locations" :key="i">
          <p v-if="loc?.description">{{ loc.description }}</p>
          <iframe
            v-if="loc?.iframe_url"
            :src="loc.iframe_url"
            width="600"
            height="450"
            style="border: 0"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
          ></iframe>
          <p v-for="(source_, i) in loc.sources" :key="i">
            <span v-if="source_.type"
              >({{ source_.type[0] }}, {{ source_.type[1] }})
            </span>
            <span
              v-if="source_?.source"
              v-html="makeLinksClickable(source_.source)"
            ></span>
          </p>
          <p v-if="loc?.comments">{{ loc.comments }}</p>
        </div>
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
  </div>

  <PopUpManager ref="popUpManager" />
</template>

<style scoped>
@import "@/assets/common.css";

/* Container and header */
.ed-div {
  margin: 1em;
  border-radius: 5px;
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

/* Unified table title styling (merged duplicates) */
.ed-table-title {
  text-align: center !important;
  font-size: larger;
  font-weight: 700;
  padding-bottom: 0.3em;
  background-color: var(--scarlet-dark);
  color: var(--grey-vibrant);
}

p {
  margin: 0;
}

/* Description / Sources */
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

/* Search row (input + regex toggle + results) */
.ed-input {
  margin-top: 1em;
  margin-left: 1em;
}
.ed-search-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.ed-search-row .ed-input {
  margin-top: 0;
  margin-left: 0;
}
.ed-regex-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  font-weight: 700;
  margin-left: 0.25rem;
}
.ed-regex-label {
  font-size: 0.95rem;
  line-height: 1;
}
.ed-results {
  margin-left: 0.25rem;
  font-weight: 600;
}

/* Popup button (single definition) */
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

/* Styles for the virtualized circle list (merged .ed-vlist-component rules) */
.ed-div-table {
  margin-top: 1em;
  background-color: var(--scarlet-dark);
  color: var(--grey-vibrant);
  text-align: left;
  font-size: 18px;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 20px #3b393926;
  border: 3px solid var(--scarlet-dark);
  border-radius: 5px;
}

input.ed-input {
  background-color: var(--grey-vibrant);
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0.4em 0.6em;
  border-radius: 0.25em;
}

.ed-header-table {
  width: 100%;
}
.ed-vlist {
  margin: 0 0.25em;
}

/* The vlist container must be the scroll container. Keep a single definition. */
.ed-vlist-component {
  height: 30em;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  box-sizing: border-box;
}

.ed-vlist-item {
  height: 22px;
  padding: 0;
  background-color: var(--grey-dark);
  color: var(--grey-light);
}
.ed-vlist-wrapper {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}
.ed-vlist-component table {
  table-layout: fixed;
  border-collapse: collapse;
  border-spacing: 0;
}
.ed-body-table tbody tr.ed-vlist-item {
  height: 22px !important;
}
.ed-body-table tbody tr.ed-vlist-item td,
.ed-body-table tbody tr.ed-vlist-item th,
.ed-vlist-item td,
.ed-vlist-item th {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding: 0 0.3em;
  line-height: 22px;
  height: 22px;
}

.ed-vlist-item-even {
  background-color: var(--grey-dark);
}
.ed-vlist-item-odd {
  background-color: var(--greyish-deep);
}

a.ed-event-link {
  color: var(--scarlet-soft);
}

.ed-body-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}
.ed-body-table td {
  padding: 0 0.3em;
  color: var(--grey-light);
  vertical-align: middle;
}

/* Force ed-body-table row coloring to follow the virtual index classes rather than DOM order (which changes with virtualization). */
.ed-body-table tbody tr {
  background-color: var(--grey-dark) !important;
  color: var(--grey-light) !important;
}
.ed-body-table tbody tr.ed-vlist-item-odd {
  background-color: var(--greyish-deep) !important;
}
.ed-body-table tbody tr.ed-vlist-item-even {
  background-color: var(--grey-dark) !important;
}

/* Neutralize generic nth-child rule for this table to avoid clashes */
.ed-body-table tbody tr:nth-child(odd),
.ed-body-table tbody tr:nth-child(even) {
  background-color: transparent !important;
}
</style>
