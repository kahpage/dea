<!--============================================================ ...
    Hide / Show content
... ============================================================ -->

<template>
  <div :class="['ts-div', { 'ts-open': !is_hidden }]">
    <button class="ts-button" @click="toggleVisibility" >
      <span v-if="is_hidden">⏵</span><span v-else>⏷</span>
      {{ props.button_text }}
    </button>
    <div v-if="do_prevent_load">
      <!-- using v-if -->
      <div class="ts-content" v-if="!is_hidden">
        <slot></slot>
      </div>
    </div>
    <div v-else>
      <!-- using v-show -->
      <div class="ts-content" v-show="!is_hidden">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  button_text: String,
  do_prevent_load: { type: Boolean, required: false, default: true }, // Prevent load (v-if) by default
  default_hidden: { type: Boolean, required: false, default: true }, // Hidden by default
});

const is_hidden = ref(props.default_hidden);

function toggleVisibility() {
  is_hidden.value = !is_hidden.value;
}
</script>

<style scoped>
@import "@/assets/common.css";

.ts-div {
  background-color: var(--purple-deeper);
  width: auto; /* shrink to content by default */
  max-width: 100%;
  border-radius: 1em;
  margin: 1em 0.5em; /* keep horizontal margin but allow full width */
  box-sizing: border-box;
  overflow-x: hidden; /* prevent children from causing page-level overflow */
}

.ts-div.ts-open {
  width: 100%; /* expand to full available width when open */
}

.ts-button {
    border: none;
    color: var(--grey-light);
    background-color: transparent;
    font-weight: 700;
    font-size: large;
    border-radius: 1em;
  margin: 0.5em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: calc(100% - 1em);
}

.ts-content {
  padding: 0 1em 1em 1em;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  min-width: 0; /* allow flex containers to shrink children */
  overflow-x: auto; /* enable horizontal scrolling for large content */
  overflow-y: visible;
}

.ts-content img,
.ts-content pre,
.ts-content table {
  max-width: 100%;
  box-sizing: border-box;
  overflow-wrap: break-word;
  word-break: break-word;
}

.ts-content pre {
  white-space: pre-wrap; /* allow long lines in pre to wrap */
}
</style>
