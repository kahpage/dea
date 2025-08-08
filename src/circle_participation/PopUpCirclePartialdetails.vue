<!--============================================================ ...
     Pop up for circle (partial) details
... ============================================================ -->

<template>
  <PopUpGeneric @close="$emit('close')" :title="`Circle Partial Details: ${circle_db.names[0] || 'undefined'}`">
    <div class="popup-circle-div">
      <p class="cd-aliases"> <span class="info-name">Names:</span> {{ circle_db?.names?.join(" / ") }}</p>
      <p class="cd-event"> <span class="info-name">Event:</span> 
        {{  }}
        <a
          class="cd-event-link"
          :href="
            ['/dea/event_detail/#']
              .concat(circle_db.ar_path)
              .join('/')
          "
        >
          {{ circle_db.event_name }}
        </a>
      </p>
      <div class="cd-misc" v-if="circle_db.hasOwnProperty('misc') && circle_db.misc.length > 0">
        <span class="info-name">Misc:</span>
        <ul class="cd-ul-descriptions">
          <span v-for="(misc_elem, i) in circle_db.misc" :key="i">
            <li v-for="(line, j) in misc_elem.split('\n')" :key="j">
              <span v-html="makeLinksClickable(line)"></span>
            </li>
          </span>
        </ul>
      </div>
      
      <p>Note: search results matches for any fields described above.</p>
      <p>For more details, please refer to event detail page.</p>
    </div>
  </PopUpGeneric>
</template>

<script setup>
import PopUpGeneric from '../components/PopUpGeneric.vue';
import {makeLinksClickable} from "@/assets/utils.js";

const props = defineProps({
  circle_db: {
    type: Object,
    required: true
  },
  db_path: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
p {
  margin: 0.4em 0;
}

.cd-ul-descriptions {
    list-style-type: disc;
}

.info-name {
  color: var(--orange-mild);
  font-weight: bold;
  font-size: 1.1em;
}

a.cd-event-link {
  color: var(--scarlet-soft);
  font-weight: bold;
}
</style>
