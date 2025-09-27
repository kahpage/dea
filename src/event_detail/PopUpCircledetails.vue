<!--============================================================ ...
     Pop up for circle details
... ============================================================ -->

<template>
  <PopUpGeneric @close="$emit('close')" :title="`Circle Details: ${circle_db.aliases[0] || 'undefined'}`">
    <div class="popup-circle-div">

      <p class="cd-aliases"> <span class="info-name">Names:</span> {{ circle_db?.aliases?.join(" / ") }}</p>
      <p class="cd-pen_names" v-if="circle_db.hasOwnProperty('pen_names') && circle_db.pen_names" > <span class="info-name">Pen names:</span> {{ circle_db.pen_names?.join(" / ") }}</p>
      <p class="cd-position" v-if="circle_db.hasOwnProperty('position') && circle_db.position" > <span class="info-name">Booth position:</span> {{ circle_db.position }}</p>
      
      <div class="cd-links" v-if="circle_db.hasOwnProperty('links') && circle_db.links" >
        <span class="info-name">Links:</span>
        <ul class="cd-ul-links">
          <li class="cd-link" v-for="(link, i) in circle_db.links" :key="i">
            <span v-html="makeLinksClickable(link)"></span>
          </li>
        </ul>
      </div>

      <div class="cd-descriptions" v-if="circle_db.hasOwnProperty('comments') && circle_db.comments" >
        <span class="info-name">Comments:</span>
        <ul class="cd-ul-descriptions">
          <li class="cd-descriptions" v-for="(desc, i) in circle_db.comments.split('\n')" :key="i">
            {{desc}}
          </li>
        </ul>
      </div>

      <div v-if="circle_db.hasOwnProperty('media')">
        <span class="info-name">Media:</span>
        <MediaGrid :media_list="circle_db.media" :media_folder_path="[PATH_DB_TO_EXPORT].concat(db_path).concat(['media']).join('/')"/>
      </div>

    </div>
  </PopUpGeneric>
</template>

<script setup>
import PopUpGeneric from '../components/PopUpGeneric.vue';
import MediaGrid from '../components/MediaGrid.vue';
import {makeLinksClickable, PATH_DB_TO_EXPORT} from "@/assets/utils.js";

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
</style>
