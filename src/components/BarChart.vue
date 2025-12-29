<template>
  <span
    :style="{
      width: props.width,
      height: props.height,
      display: 'flex',
      box_sizing: 'border-box',
    }"
  >
    <div class="chart-div">
      <h3 class="chart-title">{{ props.title }}</h3>
      <h1 class="bar-hover-display" :style="{ opacity: isHovered ? 0.8 : 0 }">
        <div class="hovered-name">
          <div v-if="hoveredBarPrefix" class="hovered-prefix">
            {{ hoveredBarPrefix }}
          </div>
          <div class="hovered-main">{{ hoveredBarName }}</div>
        </div>
        <div class="hovered-value">{{ hoveredBarValue }}</div>
      </h1>
      <div class="chart-container">
        <ul class="chart">
          <li
            v-for="(item, i) in props.data"
            :key="item.name + '-' + i"
            class="bar-container"
            :class="{ clickable: item && item.url }"
            @mouseover="onBarHover(item.name, item.value, item.prefix)"
            @mouseout="onBarLeave()"
          >
            <a
              v-if="item && item.url"
              :href="item.url"
              target="_blank"
              rel="noopener"
              class="bar-link"
            >
              <div
                class="bar"
                :style="`height: ${
                  ((item.value ? item.value : 0) / getMaxitemvalue) * 100
                }%;`"
              ></div>
              <span class="bar-name">{{ item.name }}</span>
            </a>
            <template v-else>
              <div
                class="bar"
                :style="`height: ${
                  ((item.value ? item.value : 0) / getMaxitemvalue) * 100
                }%;`"
              ></div>
              <span class="bar-name">{{ item.name }}</span>
            </template>
          </li>
        </ul>
      </div>
    </div>
  </span>
</template>

<script setup>
import { ref, computed } from "vue";
const props = defineProps({
  data: Array, // { value: Number, name: String, prefix: String, url: String }
  title: String,
  width: {
    type: String,
    default: "95vw",
  },
  height: {
    type: String,
    default: "20em",
  },
});
const getMaxitemvalue = computed(() => {
  if (!props.data || props.data.length === 0) {
    return 1;
  }
  let m = Math.max(...props.data.map((elem) => (elem?.value ? elem.value : 0)));
  if (m == 0) {
    return 1;
  }
  return m;
});

const isHovered = ref(false);
const hoveredBarName = ref("");
const hoveredBarPrefix = ref("");
const hoveredBarValue = ref("");

function onBarHover(name, value, prefix) {
  isHovered.value = true;
  // Only single-line names allowed; show prefix (if provided) in hover text
  const base = name === undefined || name === null ? "" : String(name);
  hoveredBarName.value = base;
  hoveredBarPrefix.value =
    prefix === undefined || prefix === null ? "" : String(prefix);
  if (value == undefined || value === null || isNaN(value)) {
    hoveredBarValue.value = "N/A";
  } else {
    hoveredBarValue.value = value;
  }
}
function onBarLeave() {
  isHovered.value = false;
  hoveredBarName.value = "";
  hoveredBarPrefix.value = "";
  hoveredBarValue.value = "";
}
// onBarClick removed in favor of native anchor links for previewability
</script>

<style scoped>
.chart-div {
  margin: 0;
  padding: 0;
  border: 5px solid var(--greyish-soft);
  background-color: var(--greyish-dark);
  border-radius: 5px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative; /* Ensure this is set to position children absolutely within */
}

.chart-title {
  margin: 0;
  padding: 0.2em;
  text-align: center;
  background-color: var(--greyish-soft);
}

.chart-container {
  flex: 1;
  width: 100%;
  padding: 0.4em;
  box-sizing: border-box;
  display: flex;
  overflow-x: auto;
}

.chart {
  display: flex;
  gap: 0.5%;
  margin: 0;
  padding: 0;
  list-style-type: none;
  height: 100%;
  align-items: flex-end;
  width: 100%;
}

.bar-container {
  flex: 1 1 0;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  position: relative;
  box-sizing: border-box;
  min-width: 0.7em;
  height: 100%;
}

.bar-container:hover {
  background: var(--greyish-mild);
}
.bar-container:hover .bar {
  background: var(--scarlet-vibrant);
}

.bar-container.clickable {
  cursor: pointer;
}

.bar-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end; /* ensure bar sits at bottom and grows upward */
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.bar {
  background: var(--scarlet-soft);
  width: 100%;
  position: relative;
  box-sizing: border-box;
}

.bar-name {
  position: absolute;
  transform: rotate(-90deg) translateX(50%);
  transform-origin: center center;
  font-size: 0.8em;
  color: var(--grey-light);
  font-weight: bold;
  white-space: nowrap;
  bottom: 0;
}

.bar-hover-display {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.2);
  padding: 0.4em 0.4em;
  border-radius: 0.5em;
  z-index: 10;
  opacity: 0;
  pointer-events: none;
}

.bar-hover-display {
  opacity: 0.8;
  transition: opacity 0.3s ease-in-out;
  text-align: center; /* center lines horizontally */
}

.hovered-name {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.1em;
  max-width: 60vw;
}

.hovered-prefix,
.hovered-main {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  text-align: center;
}

.hovered-prefix {
  font-size: 0.85em;
  opacity: 0.9;
}

.hovered-main {
  font-weight: bold;
}
</style>
