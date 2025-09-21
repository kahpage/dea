<!--============================================================ ...
    Hide / Show content
... ============================================================ -->

<template>
  <div class="ts-div">
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
    width: max-content;
    border-radius: 1em;
    margin: 1em;
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
}

.ts-content {
    padding: 0 1em 1em 1em;
    width: max-content;
}
</style>
