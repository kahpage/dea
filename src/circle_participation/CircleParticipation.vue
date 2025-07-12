<script setup>
import { useVirtualList } from "@vueuse/core";
import { computed, shallowRef } from "vue";
import { ref } from "vue";
import circle_raw_index from "@/assets/static_databases/circle_participation_index.json"; // Static database import

const keywords = ref("");

function recursive_fill_circle_index(current_raw_index, ar_path) {
  let current_circle_list = [];

  for (const db_name in current_raw_index) {
    if (Array.isArray(current_raw_index[db_name])) {
      // Not a subfolder, but a db
      let raw = current_raw_index[db_name];
      for (const key in raw) {
        raw[key]["event_ar_path"] = ar_path.concat(db_name); // add ar_path
      }
      current_circle_list = [].concat(current_circle_list, raw);
    } else {
      // A subfolder
      let raw = recursive_fill_circle_index(
        current_raw_index[db_name],
        ar_path.concat(db_name)
      );
      current_circle_list = [].concat(current_circle_list, raw);
    }
  }

  return current_circle_list;
}

const circle_index = computed(() => {
  return recursive_fill_circle_index(circle_raw_index, []);
});

const circle_index_lowered = computed(() => {
  if (
    !circle_index ||
    !circle_index.value ||
    !Array.isArray(circle_index.value)
  ) {
    return [];
  }
  return circle_index.value.map((circle) => {
    return {
      ...circle,
      names: circle.names.map((name) => name.trim().toLowerCase()), // Lowercase all names
      misc: circle.misc && Array.isArray(circle.misc)?circle.misc.map((name) => name.trim().toLowerCase()):null, // Lowercase all misc
      event_name: circle.event_name.trim().toLowerCase(), // Lowercase event name
    };
  });
});

const filtered_circles = computed(() => {
  // According to keywords
  if (
    !circle_index ||
    !circle_index.value ||
    !Array.isArray(circle_index.value)
  ) {
    return [];
  }

  let query = keywords.value.trim().toLowerCase();
  return circle_index_lowered.value.filter((circle) => {
    let matchNames = circle.names.some((name) => name.includes(query)); // Check if any name in the circle's names array includes the search query
    let matchEvent = circle.event_name.toLowerCase().includes(query); // Check for event match
    let matchMisc = circle.misc && circle.misc.some((misc) => misc.toLowerCase().includes(query));
    return matchNames || matchEvent || matchMisc; // Return true if either matches
  
  });
});

const { list, containerProps, wrapperProps, scrollTo } = useVirtualList(
  filtered_circles,
  {
    itemHeight: 22,
    // overscan: 10,
  }
);

function searchUpdate () {
  keywords.value = event.target.value;
  scrollTo(0);
}
</script>

<template>
  <!-- Title -->
  <head><title>dea | Circle Participation</title></head>

  <div class="header-title">Circle Participation</div>
  <div class="header">List of participating circles registered in the database.</div>
  
  <input class="cp-input" :value="keywords" @input="searchUpdate" placeholder="Keywords" /> ({{filtered_circles?.length}} results)

  <div class="cp-div">
    
    <table class="cp-header-table">
      <thead>
        <tr>
          <th colspan="4" class="cp-table-title">
            Participating circles
          </th>
        </tr>
        <tr>
          <th>Names / Pen Names</th>
          <th >Event</th>
        </tr>
      </thead>
    </table>

      <div class="cp-vlist">
        <div v-bind="containerProps" class="cp-vlist-component">
          <div v-bind="wrapperProps">
            <div
              v-for="(circle, i) in list"
              :key="i"
              class="cp-vlist-item"
            > 
              <div :class="circle.index % 2 === 0 ? 'cp-vlist-item-even' : 'cp-vlist-item-odd'">
                <!-- {{ circle }} -->
                <table>
                  <tbody>
                    <tr>
                      <th>{{ circle.data.names.join(", ") }}</th>
                      <th>
                        <a class="cp-event-link" :href="['/dea/event_detail/#'].concat(circle.data.event_ar_path).concat(circle.data.event_name).join('/')">
                          {{ circle.data.event_name }}
                        </a>
                      </th>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<style scoped>

  .cp-div {
    margin: 1em;
    background-color: var(--orange-dark);
    color: var(--grey-vibrant);
    text-align: left;
    font-size: 18px;
    font-family: Arial, sans-serif;
    box-shadow: 0 0 20px #3b393926;
    border: 3px solid var(--orange-dark);
    border-radius: 5px;
  }
  
  .cp-header-table {
    width: 100%;
  }

  .cp-table-title {
    font-size: larger;
    text-align: center;
    font-weight: 700;
  }

  .cp-vlist {
    margin: 0 0.25em;
    /* background-color: red; */
  }

  .cp-vlist-component {
    height: 30em;
  }
  
  /* Color even cp-vlist-component based on index in vlist */
  .cp-vlist-item {
    height: 22px;
    padding: 0;
    background-color: var(--grey-dark);
    color: var(--grey-light);
  }

  .cp-vlist-item-even {
  }
  .cp-vlist-item-odd {
    background-color: var(--greyish-deep);
  }

  .cp-input {
    margin-left: 1em;
  }

  th:nth-child(2) {
    text-align: right;    
    padding-right: 1em;
  }
  
  table {
    width: 100%;
  }

  tr {
    padding: 0 0.3em;
    color: var(--grey-light);
    width: 100%;
  }

  a.cp-event-link {
    color: var(--scarlet-soft);
  }
</style>
