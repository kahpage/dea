<!--============================================================ ...
     Header for navigation
... ============================================================ -->

<template>
  <!-- Navigation Links -->
  <nav class="navigation">
    <div class="navigation-buttons">
      <a href="/dea/" class="navigation-button">Home</a>
      <a href="/dea/event_list/" class="navigation-button">Event list</a>
      <a href="/dea/circle_participation/" class="navigation-button">Circles</a>
      <a href="/dea/calendar/" class="navigation-button">Calendar</a>
      <a href="/dea/about/" class="navigation-button">About</a>
    </div>
    <div class="navigation-right">
      <div class="navigation-toggles">
        <label
          class="switch"
          v-for="(state, key) in toggles"
          :key="key"
          :id="`toggle_${state}`"
          :title="'Toggle ' + state"
          @change="onToggleUpdate"
        >
          <input type="checkbox" v-model="toggle_states[state]" />
          <span class="slider round"></span>
        </label>
      </div>
      <div class="navigation-title">dea</div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  toggles: { type: Array, required: false },
});

const toggle_states = ref({});

const emits = defineEmits(["onToggleUpdate"]);

function onToggleUpdate() {
  emits("onToggleUpdate", toggle_states);
}
</script>

<style scoped>
@import "@/assets/common.css";

.navigation {
  background-color: var(--color-navigation-background);
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100;
  padding: 0 1rem;
  margin: 0;
}

.navigation-buttons {
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
}

.navigation-button {
  color: var(--vt-c-text-dark-2);
  text-decoration: none; /* Remove underline from links */
  padding: 0.5rem;
  border-radius: 0.2rem;
}

.navigation-button:hover {
  background-color: var(--green-mild);
  color: var(--grey-vibrant);
}

.navigation-right {
  display: flex;
  flex-direction: row;
}

.navigation-title {
  padding: 0.5rem;
  color: var(--gray-mild);
  font-weight: bold;
}

.navigation-toggles {
  padding: 0.5em 0;
}
</style>
