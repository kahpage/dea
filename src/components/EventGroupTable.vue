<!--============================================================ ...
    Table for one event group
... ============================================================ -->

<template>
  <div class="eg-div">
    <a class="eg-title" :href='eg_href'>{{ headerTitles }}</a>

    <div v-if="props.show_details && props.event_group_db.hasOwnProperty('links') && Array.isArray(props.event_group_db.links)" class="eg-links">
      Links: <span v-html="makeLinksClickable(props.event_group_db?.links.join(', '))"></span>
    </div>
    <!-- ===== Description ===== -->
    <ToggleShow class="ts-description" v-if="props.event_group_db?.description" :button_text="'Description'" :default_hidden="false" >
      <p v-for="(row, i) in props.event_group_db.description.split('\n')" :key="i">
        <span v-html="makeLinksClickable(row)"></span>
      </p>
    </ToggleShow>

    <table>
      <thead>
        <tr><th>Event</th>      <th>Date</th></tr>
      </thead>
      <tbody>
        <tr v-for="(val, i) in descriptionEvents" :key="i">
            <th>
              {{val.dates}}
            </th>
            <th>
              <a :href="ar_path_complete.concat(val.name).join('/')">{{val.name}}</a>
            </th>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from "vue";
import {makeLinksClickable} from "@/assets/utils.js";
import ToggleShow from "@/components/ToggleShow.vue";

const props = defineProps({
  event_group_db: Object,
  eg_ar_path: Array, // Of containing event group
  show_details: { type: Boolean, required: false, default: false }, // If should show details such as links or notes
});

const headerTitles = computed(() => {
  if (!props.event_group_db.hasOwnProperty("aliases")) {return ""};
  return props.event_group_db["aliases"].join(" / ");
});

const ar_path_complete = computed(() => { // Complete ar_path to construct target url
  return ["/dea/event_detail/#"].concat(props.eg_ar_path);
});

const descriptionEvents = computed(() => {
      if (!props.event_group_db.hasOwnProperty("events")) {
        return [];
      }
      
      let events = props.event_group_db["events"];
      let descs = []; // Description, of format { dates: "", name: "" };
      
      // events is an object with event aliases as keys
      Object.keys(events).forEach(eventAlias => {
        let event_desc = { dates: "", name: "" };
        event_desc.name = eventAlias; // The key is the event alias/name
        if ("dates" in events[eventAlias]) {
          event_desc.dates = events[eventAlias].dates;
        }
        descs.push(event_desc);
      });

      return descs
    });

const eg_href = computed(() => {
  return ["/dea/event_group_detail/#"].concat(props.eg_ar_path).join("/");
});
</script>

<style scoped>
  @import '@/assets/common.css';

  .eg-div {
    margin: 1em;
    /* border: 2px solid var(--greyish-soft); */
    background-color: var(--greyish-dark);
    width: auto;
  }

  a.eg-title {
    margin: 1em 0;
    font-size: x-large;
    color: var(--green-mild);
    font-family: "Segoe UI";
    font-weight: 700;
  }

  table {
    width: auto;
    margin: 1em 0;
    font-size: 18px;
    font-family: Arial, sans-serif;
    box-shadow: 0 0 20px rgba(59, 57, 57, 0.15);
    border: 3px solid var(--green-dark);
    border-radius: 5px;
    overflow: hidden;
    text-align: left;
    border-collapse: separate; 
    border-spacing: 0;
  }

  thead tr {
    background-color: var(--green-dark);
    color: var(--grey-vibrant);
    text-align: left;
  }

  th {
    padding: 0 0.3em;
    text-align: left;
  }

  tr:nth-child(even) {
    background-color: var(--grey-dark);
  }

  .eg-links {}

  .ts-description {
    padding: 0;
    margin: 0;
    margin-top: 1em;
  }

  .ts-description p {
    margin: 0 0;
    word-wrap: break-word;
  }
</style>
