<!--============================================================ ...
    Grid to display media
... ============================================================ -->

<template>
  <div class="media-div"
    v-if="!props.media_list || Array.isArray(props.media_list) & (props.media_list.length == 0)"
  >
    (None)
  </div>
  <div v-else class="media-div">
    <div class="media">
      <div class="medium" v-for="(media, index) in props.media_list" :key="index">

        <!-- Image -->
        <img class="format-image" v-if="isImage(media)" 
          :src="props.media_folder_path + '/' + media.path"
          :alt="'Image ' + media.path"
          style="max-width: 100%; height: auto"
        />

        <!-- Other format -->
        <div v-else>
          <a class="format-other" :href="props.media_folder_path + '/' + media.path" target="_blank" title="Other file type">
            {{ media.path }}
          </a>
        </div>

        <div v-if="media.hasOwnProperty('sources')">
          <div v-for="(source_, j) in media.sources" :key="j">
            <span v-if="source_.hasOwnProperty('type')"
              >({{ source_["type"][0] }}, {{ source_["type"][1] }})</span
            >
            <br />
            <span v-html="makeLinksClickable(source_.source)"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {makeLinksClickable} from "@/assets/utils.js";

const props = defineProps({
  media_list: Array, // List of media objects
  media_folder_path: String, // Path to the folder containing media files
});

function isImage(media) {
  return media && media.path && /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(media.path.toLowerCase());
}

</script>

<style scoped>
@import "@/assets/common.css";

/* media */
.media-div {
  padding: 1em;
  box-sizing: border-box; 
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
  gap: 1em;
  justify-content: center;
  overflow-y: scroll;
  background-color: var(--greyish-dark);
  max-height: 40vh;
  border: 1px solid var(--greyish-soft);
}

.medium {
  margin-top: 0.5em;
}

.format-image {}
a.format-other{
  color: var(--green-soft);
  text-decoration: none;
  font-weight: bold;
}

</style>
