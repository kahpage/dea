<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
  import { ref, computed } from "vue";
  import circle_raw_index from '@/assets/static_databases/circle_participation_index.json' // Static database import
  import { useVirtualList } from '@vueuse/core'

  const keywords= ref("")

  function recursive_fill_circle_index(current_raw_index, ar_path) {
    let current_circle_list = []

    for (const db_name in current_raw_index) {
      if (Array.isArray(current_raw_index[db_name])) { // Not a subfolder, but a db
        let raw = current_raw_index[db_name]
        for (const key in raw) {
          raw[key]["event_ar_path"] = ar_path.concat(db_name) // add ar_path
        }
        current_circle_list = [].concat(current_circle_list, raw)
      } else { // A subfolder
        let raw = recursive_fill_circle_index(current_raw_index[db_name], ar_path.concat(db_name))
        current_circle_list = [].concat(current_circle_list, raw)
      }
    }
     
    return current_circle_list
  }
  
  const circle_index = computed(() => {
    return recursive_fill_circle_index(circle_raw_index, [])
  })

  const circle_index_lowered = computed(() => {
    if (!circle_index || !circle_index.value || !Array.isArray(circle_index.value)) {return []}
    return circle_index.value.map(circle => {
      return {
        ...circle,
        names: circle.names.map(name => name.trim().toLowerCase()) // Lowercase all names
      }
    })
  })

  const filtered_circles = computed(() => { // According to keywords
    if (!circle_index || !circle_index.value || !Array.isArray(circle_index.value)) {return []}

    let query = keywords.value.trim().toLowerCase();
    return circle_index_lowered.value.filter(circle => {
      return circle.names.some(name => name.includes(query)); // Check if any name in the circle's names array includes the search query
    });
  })
  
  const { vlist, vcontainerProps, vwrapperProps } = useVirtualList(
    filtered_circles,
    {
      itemHeight: 22,
    }
  )
</script>

<template>
    <!-- Title -->
    <head><title>dea | Circle Participation</title></head>

    <div class="header-title">Circle Participation</div>
    <div class="header">List of participating circles registered in the database.</div>

    <div class="cp-div">
      <input v-model="keywords" placeholder="Keywords"> ({{ filtered_circles?.length }} results)

      <div v-bind="vcontainerProps" style="height: 300px">
        <div v-bind="vwrapperProps">
          <div v-for="(circle, i) in vlist" :key="i" style="height: 22px">
            Row: {{ circle }}
          </div>
        </div>
      </div>

    </div>








    
    <div class="cp-div">
      <input v-model="keywords" placeholder="Keywords"> ({{ filtered_circles?.length }} results)

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