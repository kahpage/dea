<!--============================================================ ...
    An Event group
... ============================================================ -->

<template>
  <div>
    <!-- Category header. Only if name!='' (root)-->
    <div v-if="ec_name" class="header-title">
      <section :id="ec_name"></section>
      {{ ec_name }}
      <span v-if="event_categ_count >= 0">({{ event_categ_count }})</span>
    </div>

    <div class="ec-container">
      <!-- Event groups for this category -->
      <div v-for="(val, i) in categoryGroups" :key="i">
        <section :id="i"></section>
        <EventGroupTable :event_group_db="val" :eg_ar_path="ar_path.concat(i)" :event_index="i" />
      </div>
      
      <!-- Sub categories -->
      <div v-for="(sub_categ_desc, i) in eventCategChildrenListIndexes" :key="i">
        <EventCategory
          v-if="sub_categ_desc.index != undefined"
          :event_list_index="sub_categ_desc.index"
          :ec_name="sub_categ_desc.name"
          :ar_path="props.ar_path.concat(sub_categ_desc.name)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import EventGroupTable from "./EventGroupTable.vue";
import { computed } from "vue";
import axiosInstance from "@/axios/axios_config.js";

const props = defineProps({
  event_list_index: Object,
  ec_name: String,
  ar_path: Array, // Array representation of path to current category
});

const event_categ_count = computed(() =>
  props.event_list_index.hasOwnProperty("@count")
    ? props.event_list_index["@count"]
    : -1
);

const eventCategChildrenListIndexes = computed(() => {
  if (props.event_list_index == undefined) {
    return [];
  }
  /* dict of indexes for the children groups {categ_name: categ_index}*/
  let out_list = [];

  for (const key in props.event_list_index) {
    if (["@databases", "@count"].includes(key)) {
      continue;
    } // Exclude reserved

    let sub_categ_description = {
      // Make description dict
      index: props.event_list_index[key],
      name: key,
      count: props.event_list_index[key].hasOwnProperty("@count")
        ? props.event_list_index[key]["@count"]
        : -1,
    };

    out_list.push(sub_categ_description);
  }

  return out_list;
});

const categoryGroups = computed(() => {
  if (!props.event_list_index.hasOwnProperty("@databases") || !props.event_list_index["@databases"]) {return [];}
  return props.event_list_index["@databases"];
});

</script>

<style scoped>
@import "@/assets/common.css";

.ec-container {
  margin: 0.5em 0 0.5em 0.5em;
  /* border: 2px solid var(--greyish-soft); */
  background-color: var(--greyish-dark);
  width: auto;
}
</style>
