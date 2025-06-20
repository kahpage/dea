<!--============================================================ ...
    An Event group
... ============================================================ -->

<template>
  <div>
    <!-- Category header. Only if name!='' (root)-->
    <div v-if="ec_name" class="header-title">
      {{ ec_name }}
      <span v-if="event_categ_count >= 0">({{ event_categ_count }})</span>
    </div>

    <div class="ec-container">
      <!-- Event groups for this category -->
      <div v-for="(val, i) in category_groups" :key="i">
        <!-- TODO: fetch -->
        <EventGroupTable :event_group_db="val" />
      </div>

      <!-- Sub categories -->
      <div v-for="(sub_categ_desc, i) in eventCategChildrenIndexes" :key="i">
        <EventCategory
          v-if="sub_categ_desc.index != undefined"
          :event_categ_index="sub_categ_desc.index"
          :ec_name="sub_categ_desc.name"
          :ar_path="ar_path.concat([sub_categ_desc.name])"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import EventGroupTable from "./EventGroupTable.vue";
import { ref, computed, onMounted } from "vue";
import axiosInstance from "@/axios/axios_config.js";

const props = defineProps({
  event_categ_index: Object,
  ec_name: String,
  ar_path: Array,
});

const event_categ_count = computed(() =>
  props.event_categ_index.hasOwnProperty("@count")
    ? props.event_categ_index["@count"]
    : -1
);
const eventCategChildrenIndexes = computed(() => {
  if (props.event_categ_index == undefined) {
    return [];
  }
  /* dict of indexes for the children groups {categ_name: categ_index}*/
  let out_list = [];

  for (const key in props.event_categ_index) {
    if (["@databases", "@count"].includes(key)) {
      continue;
    } // Exclude reserved

    let sub_categ_description = {
      // Make description dict
      index: props.event_categ_index[key],
      name: key,
      count: props.event_categ_index[key].hasOwnProperty("@count")
        ? props.event_categ_index[key]["@count"]
        : -1,
    };

    out_list.push(sub_categ_description);
  }

  return out_list;
});

const public_path = import.meta.env.MODE == "production" ? `/dea/` : `../`; // Path of public/ folder
const category_groups = ref([]); // Databases of current category that will be fetched

async function fetch_db(db_name) {
  /* Fetch the given db */
  let ar_path_more = [`${public_path}databases`]
    .concat(props.ar_path)
    .concat([`${db_name}/${db_name}.json`]);
  let db_url = ar_path_more.join("/"); // complete path
  console.log("Fetching ", db_url);

  // Return the promise chain
  return axiosInstance
    .get(db_url)
    .then((response) => {
      if (!response.data.hasOwnProperty("aliases")) {
        return false;
      } // Check if invalid !
      category_groups.value.push(response.data);
      console.log("NEW FETCHED: ", category_groups);
      return true;
    })
    .catch((error) => {
      console.error("Error fetching data:", error); // Log any errors that occur during the fetch
      return false;
    });
}

function fetch_databases() {
  /* Fetch databases and fill category_groups */
  if (!props.event_categ_index.hasOwnProperty("@databases")) {
    console.log("Failed A ", props.event_categ_index);
    return;
  } // Nothing to load
  if (!Array.isArray(props.event_categ_index["@databases"])) {
    console.log("Failed B ", props.event_categ_index);
    return;
  } // Invalid @databases

  for (const db_name in props.event_categ_index["@databases"]) {
    fetch_db(props.event_categ_index["@databases"][db_name]);
  }
}

onMounted(() => {
  /* Run when done loading */
  fetch_databases();
});
</script>

<style scoped>
@import "@/assets/common.css";

.ec-container {
  margin: 0.5em;
  /* border: 2px solid var(--greyish-soft); */
  background-color: var(--greyish-dark);
  width: auto;
}
</style>
