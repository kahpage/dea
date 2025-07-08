<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import { ref, computed, watchEffect } from "vue";
import { useRoute } from "vue-router";
import axiosInstance from "@/axios/axios_config.js";
import makeLinksClickable from "@/assets/utils.js";
import ToggleShow from "@/components/ToggleShow.vue";

const public_path = import.meta.env.MODE == "production" ? `/dea/` : `/dea/`; // Path of public/ folder

const route = useRoute();
const props = defineProps({
  db_path: String,
});

const event_data = ref(null);

const media_folder_path = computed(() => {
  return [`${public_path}databases`]
    .concat(db_path_description.value)
    .concat("media")
    .join("/");
});

const media_list = computed(() => {
  if (!event_data.value || !event_data.value.hasOwnProperty("media")) {
    return [];
  }
  return event_data.value.media;
});

const db_path_args = computed(() => {
  return props.db_path ? props.db_path.split("/").filter(Boolean) : [];
});

const db_path_description = computed(() => {
  // file path description
  return db_path_args.value.slice(0, -1);
});

const db_path_event_name = computed(() => {
  // event entry inside the json
  return db_path_args.value.length > 0
    ? db_path_args.value[db_path_args.value.length - 1]
    : null;
});

async function fetch_db() {
  // Construct the URL using the parameters
  event_data.value = {};
  let db_name = db_path_description.value[db_path_description.value.length - 1];
  let ar_path_more = [`${public_path}databases`]
    .concat(db_path_description.value)
    .concat([`${db_name}.json`]);
  let db_url = ar_path_more.join("/"); // complete path
  console.log(`Fetching ${db_url}...`); // Log the fetched data

  try {
    const response = await axiosInstance.get(db_url);
    if (!response.data.hasOwnProperty("aliases")) {
      return; // Check if the response is invalid
    }

    console.log("NEW FETCHED: ", response.data); // Log the fetched data
    return get_event_db(response.data);
  } catch (error) {
    console.error("Error fetching data:", error); // Log any errors that occur during the fetch
  }
}

function get_event_db(response_data) {
  if (!response_data.hasOwnProperty("events")) {
    return; // Check if the response is invalid
  }
  if (!Array.isArray(response_data["events"])) {
    return; // Check if the response is invalid
  }

  for (const cur_event of response_data["events"]) {
    if (
      !cur_event.hasOwnProperty("aliases") ||
      !Array.isArray(cur_event["aliases"])
    ) {
      continue; // Check if the response is invalid
    }
    if (!cur_event["aliases"].includes(db_path_event_name.value)) {
      continue;
    }

    event_data.value = cur_event;
    return;
  }
}

// Watch for changes in db_path_description and db_path_event_name
watchEffect(async () => {
  if (db_path_description.value && db_path_event_name.value) {
    console.log("Url change detected, now fetching new event data...");
    const data = await fetch_db(
      db_path_description.value,
      db_path_event_name.value
    );
  }
});
</script>

<template>
  <!-- Title -->
  <head>
    <title>dea | Event Detail</title>
  </head>

  <div class="header-title">Event detail</div>
  <div v-if="!props.db_path" class="header">
    Invalid database to fetch: "{{ props.db_path }}"
  </div>
  <div v-else>
    <div v-if="!event_data || !event_data.hasOwnProperty('aliases')">Loading database {{ props.db_path }}...</div>
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

        <div v-if="event_data?.links && Array.isArray(event_data.links)" class="ed-links">
          Links: <span v-html="makeLinksClickable(event_data.links.join(', '))"></span>
        </div>
        
      <!-- ===== Notes ===== -->
      <ToggleShow
        class="ts-notes"
        :button_text="'Notes'"
        v-if="event_data?.notes"
        :default_hidden="false"
      >
        <div class="ts-notes-div">
          <p v-for="(line, i) in event_data.notes.split('\n')" :key="i">
            {{ line }}
          </p>
        </div>
      </ToggleShow>

        <!-- ===== CIRCLE LIST ===== -->
        <div
          v-if="
            event_data?.circles &&
            Array.isArray(event_data.circles) &&
            event_data.circles.length > 0
          "
        >
          <table>
            <thead>
              <tr>
                <th colspan="5" class="ed-table-title">
                  Participating circles
                </th>
              </tr>
              <tr>
                <th>Position</th>
                <th>Aliases</th>
                <th>Pen Names</th>
                <th>links</th>
                <th>media</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(circle, i) in event_data.circles" :key="i">
                <th>{{ circle?.position ?? "" }}</th>
                <th>
                  <span
                    v-if="
                      circle &&
                      circle.hasOwnProperty('aliases') &&
                      Array.isArray(circle['aliases'])
                    "
                    >{{ circle?.aliases?.join(" / ") ?? "" }}</span
                  >
                </th>
                <th>{{ circle?.pen_names?.join(" / ") ?? "" }}</th>
                <th>
                  <span
                    v-html="makeLinksClickable(circle?.links?.join(', ') ?? '')"
                  ></span>
                </th>
                <th>
                  <span v-if="circle.hasOwnProperty('media')">
                    <a v-for="(m, i) in circle.media" :key="i" 
                    :href="[`${public_path}databases`].concat(db_path_description).concat(['media', m.path]).join('/')">
                      {{ i+1 }}
                    </a>
                  </span>
                </th>
              </tr>
            </tbody>
          </table>
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
        v-if="event_data && event_data.hasOwnProperty('comments')"
      >
        <p v-for="(row, i) in event_data.comments.split('\n')" :key="i">
          {{ row }}
        </p>
      </ToggleShow>
      
      <!-- ===== MEDIA ===== -->

      <ToggleShow class="ts-sources" :button_text="'Media'" v-if="event_data">
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

.ed-div {
  padding: 1em;
  /* border: 2px solid var(--greyish-soft); */
  background-color: var(--greyish-dark);
  width: auto;
}

.ed-header {
  color: var(--scarlet-vibrant);
  font-weight: 700;
  font-size: x-large;
}

.ed-dates {
  color: var(--grey-vibrant);
  font-style: italic;
}

a.ed-parent {
  color: var(--grey-soft);
  font-style: italic;
}

table {
  width: auto;
  margin: 1em 0;
  font-size: 18px;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 20px rgba(59, 57, 57, 0.15);
  border: 3px solid var(--scarlet-dark);
  border-radius: 5px;
  overflow: hidden;
  text-align: left;
  border-collapse: separate;
  border-spacing: 0;
}

thead {
  background-color: var(--scarlet-dark);
  color: var(--grey-vibrant);
  text-align: left;
}

th {
  padding: 0 0.3em;
  text-align: left;
  color: var(--grey-light);
}

tbody tr:nth-child(odd) {
  background-color: var(--grey-dark);
}
.ed-table-title {
  font-size: larger;
  text-align: center;
}

.ts-sources {
  margin-left: 1em;
  width: min-content;
}

/* event group media */
.ed-media-div {
  padding: 1em;
  box-sizing: border-box;
  text-wrap: wrap;
  word-wrap: break-word;
}

.ed-media {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
  gap: 1em;
  justify-content: center;
}

.ed-media-div img {
  width: 100%;
  height: auto;
  display: block;
}

.ts-notes {
  margin-left: -0.5em;
  max-width: 95%;
}

.ts-notes-div {
  width: 95%;
}

.ts-notes-div p {
  word-wrap: break-word;
}
</style>
