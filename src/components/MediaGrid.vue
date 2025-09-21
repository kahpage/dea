<!--============================================================ ...
    Grid to display media
... ============================================================ -->

<template>
  <div
    class="media-div"
    v-if="
      !props.media_list ||
      Array.isArray(props.media_list) & (props.media_list.length == 0)
    "
  >
    (None)
  </div>
  <div v-else class="media-div">
    <div class="media">
      <div
        class="medium"
        v-for="(media, index) in props.media_list"
        :key="index"
      >
        <!-- Link (externally hosted media) -->
        <div v-if="media.path.startsWith('http')">
          <a
            class="format-link"
            :href="props.media_folder_path + '/' + media.path"
            target="_blank"
            title="External link to media"
          >
            <span class="format-link-arrow">⭷</span>
            {{
              media.path
                .replace(/^\/+|\/+$/g, "")
                .split("/")
                .at(-1)
            }}
          </a>
        </div>

        <!-- Image -->
        <div v-else-if="isImage(media)">
          <a
            class="format-image-link"
            :href="props.media_folder_path + '/' + media.path"
            target="_blank"
            :title="'Image ' + media.path"
          > {{ media.path }}</a><br />
          <img
            class="format-image"
            :src="props.media_folder_path + '/' + media.path"
            :alt="'Image ' + media.path"
            style="max-width: 100%; height: auto"
          />
        </div>

        <!-- Other format -->
        <div v-else>
          <a
            class="format-other"
            :href="props.media_folder_path + '/' + media.path"
            target="_blank"
            title="Other file type"
          >
            {{ media.path }}
          </a>
        </div>

        <div v-if="media?.sources"> <!-- Sources -->
          <div v-for="(source_, j) in media.sources" :key="j">
            <span v-if="source_.hasOwnProperty('type')"
              >({{ source_["type"][0] }}, {{ source_["type"][1] }})</span
            >
            <br v-if="j < media.sources.length - 1"/>
            <span v-html="makeLinksClickable(source_.source)"></span>
          </div>
        </div>
        <div v-if="media?.comments"> <!-- Comments -->
          <div v-for="(row, j) in media.comments.split('\n')" :key="j">
            <p><span v-html="makeLinksClickable(row)"></span></p>
          </div>
        </div>
        <hr v-if="index < props.media_list.length - 1" />
        <!-- Exclude last -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { makeLinksClickable } from "@/assets/utils.js";

const props = defineProps({
  media_list: Array, // List of media objects
  media_folder_path: String, // Path to the folder containing media files
});

function isImage(media) {
  return (
    media &&
    media.path &&
    /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(media.path.toLowerCase())
  );
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
  max-height: 70vh;
  border: 1px solid var(--greyish-soft);
  max-width: 95vw;
}

.media-div hr {
  border: none;
  border-top: 1px solid var(--greyish-soft);
  margin: 0.5em 0;
}

.medium {
  margin-top: 0.5em;
}

a.format-link {
  color: var(--green-soft);
  text-decoration: none;
  font-weight: bold;
}
.format-link-arrow {
  color: var(--green-soft);
}

a.format-link:hover {
  text-decoration: underline;
}

a.format-image-link {
  color: var(--purple-soft);
}
.format-image {
}

.format-other {
  color: var(--scarlet-soft);
}
a.format-other {
  color: var(--scarlet-soft);
  text-decoration: none;
  font-weight: bold;
}
a.format-other:hover {
  text-decoration: underline;
}
</style>
