<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
  import { ref, computed } from "vue";
  import circle_index from '@/assets/static_databases/circle_participation_index.json' // Static database import

  const keywords= ref("")

  const filtered_circles = computed(() => { // According to keywords
      let query = keywords.value.trim().toLowerCase();
      return circle_index.filter(circle => {
        return circle.names.some(name => name.trim().toLowerCase().includes(query)); // Check if any name in the circle's names array includes the search query
      });
  })

</script>

<template>
    <!-- Title -->
    <head><title>dea | Circle Participation</title></head>

    <div class="header-title">Circle Participation</div>
    <div class="header">List of participating circles registered in the database.</div>

    <div class="cp-div">
      <input v-model="keywords" placeholder="Keywords">

      <table class="cp-table">
        <thead>
          <tr>
            <th colspan="4" class="cp-table-title">
              Participating circles
            </th>
          </tr>
          <tr>
            <th>Names / Pen Names</th>
            <th>Event</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(circle, i) in filtered_circles" :key="i">
            <th>
              {{ circle.names.join(" / ") }}
            </th>
            <th>
              <a class="cp-event-link" :href="['/dea/event_detail/#'].concat(circle.event_ar_path).concat(circle.event_name).join('/')">
                {{ circle.event_name }}
              </a>
            </th>
          </tr>
        </tbody>
      </table>
    </div>

    <hr>
</template>

<style>
    @import '@/assets/common.css';

  .cp-div {
    padding: 1em;
  }
    
  table {
    width: 100%;
    margin: 1em 0;
    font-size: 18px;
    font-family: Arial, sans-serif;
    box-shadow: 0 0 20px #3b393926;
    border: 3px solid var(--orange-dark);
    border-radius: 5px;
    overflow: hidden;
    text-align: left;
    border-collapse: separate;
    border-spacing: 0;
  }

  thead {
    background-color: var(--orange-dark);
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
  .cp-table-title {
    font-size: larger;
    text-align: center;
    font-weight: 700;
  }

  a.cp-event-link {
    color: var(--scarlet-soft);
  }

</style>