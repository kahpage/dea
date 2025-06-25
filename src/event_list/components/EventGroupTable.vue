<!--============================================================ ...
    Table for one event group
... ============================================================ -->

<template>
  <div class="eg-div">
    <a class="eg-title">{{ headerTitles }}</a>

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
    <!-- {{  props.ar_path}} -->
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  event_group_db: Object,
  eg_ar_path: Array, // Of containing event group
});

const headerTitles = computed(() => {
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

      events.forEach(event => {
        let event_desc = { dates: "", name: "" };
        if ("dates" in event) {
          event_desc.dates = event.dates;
        }
        if ("aliases" in event && event["aliases"].length > 0) {
          event_desc.name = event["aliases"][0];
        }
        descs.push(event_desc);
      });

      return descs
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

  .eg-title {
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
</style>
