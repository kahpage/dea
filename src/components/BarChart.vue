<template>
  <span :style="{ width: props.width, height: props.height, display: 'flex' }">
    <div class="chart-div">
      <h3 class="chart-title">{{ props.title }}</h3>
      <div class="chart-container">
        <ul class="chart">
          <li
            v-for="(item, i) in props.data"
            :key="item.name"
            class="bar"
            :style="`height: ${(item.value / getMaxitem) * 100}%`"
          >
            <span class="bar-name">{{ item.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </span>
</template>

<script setup>
import { computed } from "vue";
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
const getMaxitem = computed(() => {
  if (!props.data || props.data.length === 0) {
    return 1;
  }
  return Math.max(...props.data.map((elem) => (elem?.value ? elem.value : 0)));
});
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

.bar {
  background: var(--scarlet-soft);
  flex: 1 1 0; /* Allow bars to grow and shrink as needed */
  display: flex;
  align-items: flex-end;
  justify-content: center;
  position: relative;
  box-sizing: border-box;
  min-width: 0.7em; /* Allow bars to shrink below their intrinsic width */
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

</style>
