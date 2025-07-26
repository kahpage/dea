<template>
  <span :style="{ width: props.width, height: props.height, display: 'flex', box_sizing: 'border-box'}">
    <div class="chart-div">
      <h3 class="chart-title">{{ props.title }}</h3>
      <h1 class="bar-hover-display" :style="{ opacity: isHovered ? 0.8 : 0 }">
        {{ hoveredBarName }}: {{ hoveredBarValue }}
      </h1>
      <div class="chart-container">
        <ul class="chart">
          <li
            v-for="(item, i) in props.data"
            :key="item.name"
            class="bar-container"
            @mouseover="onBarHover(item.name, item.value)"
            @mouseout="onBarLeave()"
          >
            <div
              class="bar"
              :style="`height: ${((item.value ? item.value : 0) / getMaxitemvalue) * 100}%;`"
            ></div>
            <span class="bar-name">{{ item.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </span>
</template>

<script setup>
import { ref, computed } from "vue";
const props = defineProps({
  data: Array,
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
const hoveredBarValue = ref("");

function onBarHover(name, value) {
  isHovered.value = true;
  hoveredBarName.value = name;
  if (value == undefined || value === null || isNaN(value)) {
    hoveredBarValue.value = "N/A";
  } else {
    hoveredBarValue.value = value;
  }
}
function onBarLeave() {
  isHovered.value = false;
}
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
}
</style>
