<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import { ref, computed, watchEffect, useTemplateRef, markRaw } from "vue";
import axiosInstance from "@/axios/axios_config.js";
import {
  makeLinksClickable,
  PATH_DB_TO_EXPORT,
  fetch_url,
} from "@/assets/utils.js";
import ToggleShow from "@/components/ToggleShow.vue";
import SearchableVirtualList from "@/components/SearchableVirtualList.vue";

import PopUpManager from "@/components/PopUpManager.vue";
import MediaGrid from "@/components/MediaGrid.vue";
import PopUpCircledetails from "./PopUpCircledetails.vue";

const props = defineProps({
  db_path: String,
});

const event_data = ref(null);
const event_data_state = ref("loading"); // 'loading', 'loaded', 'error'

async function fetch_ed_db() {
  fetch_url({
    url: [PATH_DB_TO_EXPORT].concat(db_path_args.value).join("/") + ".json",
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

const db_path_args = computed(() => {
  return props.db_path ? props.db_path.split("/").filter(Boolean) : [];
});

function circleSearchText(circle) {
  const toText = (value) => {
    if (Array.isArray(value)) {
      return value
        .map((entry) => (entry === null || entry === undefined ? "" : String(entry).trim()))
        .filter(Boolean)
        .join(" / ");
    }
    if (value === null || value === undefined) return "";
    return String(value).trim();
  };

  return [
    toText(circle.aliases),
    toText(circle.pen_names),
    toText(circle.comments),
    toText(circle.position),
    toText(circle.links),
  ]
    .filter(Boolean)
    .join("\t");
}

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
        <SearchableVirtualList
          class="ed-vlist"
          contour-color="var(--scarlet-dark)"
          rows-color="var(--grey-dark)"
          :items="event_data.circles"
          :search-text-getter="circleSearchText"
          :item-height="22"
          :regex-empty-returns-all="true"
        >
          <template #header>
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
          </template>

          <template #default="{ list }">
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
                    v-bind="vitem.rowProps"
                  >
                    <td style="text-align: center">
                      <button
                        class="ed-popup-button"
                        @click="popupCircleDetails(vitem.data)"
                        title="Show circle details"
                      >
                        🡵
                      </button>
                    </td>
                    <td>
                      {{ vitem.data.position ?? "" }}
                    </td>
                    <td>
                      {{
                        Array.isArray(vitem.data.aliases)
                          ? vitem.data.aliases.join(" / ")
                          : vitem.data.aliases || ""
                      }}
                    </td>
                    <td>
                      {{
                        Array.isArray(vitem.data.pen_names)
                          ? vitem.data.pen_names.join(" / ")
                          : vitem.data.pen_names || ""
                      }}
                    </td>
                    <td>
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
          </template>
        </SearchableVirtualList>
      </div>
      <!-- ===== SOURCES ===== -->
      <ToggleShow :button_text="'Sources'" v-if="event_data?.sources">
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
        :button_text="'Comments'"
        v-if="event_data && event_data?.comments"
      >
        <p v-for="(row, i) in event_data.comments.split('\n')" :key="i">
          {{ row }}
        </p>
      </ToggleShow>

      <!-- ===== Location ===== -->
      <ToggleShow :button_text="'Location'" v-if="event_data?.locations">
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
      <ToggleShow :button_text="'Media'" v-if="event_data">
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

/* Description */
.ts-description-div {
  width: 100%;
}
.ts-description-div p {
  word-wrap: break-word;
}

/* Popup button (single definition) */
.ed-popup-button {
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
.ed-popup-button:hover {
  color: var(--orange-vibrant);
}

/* Styles for the virtualized circle list (merged .ed-vlist-component rules) */
.ed-div-table {
  margin-top: 1em;
  color: var(--grey-vibrant);
  text-align: left;
  font-size: 18px;
  font-family: Arial, sans-serif;
}

.ed-header-table {
  width: 100%;
}
.ed-vlist {
  margin: 0 0.25em;
  height: 66vh;
  max-height: 66vh;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.ed-body-table tbody tr,
.ed-body-table td,
.ed-body-table th {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding: 0 0.3em;
  line-height: 22px;
  height: 22px;
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
</style>
