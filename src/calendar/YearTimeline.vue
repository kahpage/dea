<template>
  <div class="timeline-wrapper">
    <div class="year-label">{{ year }}</div>
    <div class="timeline-container">
      <div class="timeline-line"></div>
      <div
        v-for="(month, index) in monthSeparators"
        :key="index"
        class="month-marker"
        :style="{ left: month.position + '%' }"
      >
        <div class="month-dot"></div>
        <div class="month-label" v-if="month.name">{{ month.name }}</div>
      </div>
      <div
        v-for="(event, index) in eventBars"
        :key="'event-' + index"
        class="event-bar"
        :style="event.style"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  year: {
    type: Number,
    default: new Date().getFullYear()
  },
  events_of_the_year: Array, // List of events of the year {name: event_name,date_start: date_start,date_end: date_end,was_held: was_held,ar_path: event_group_ar_path,hue: hue_event_group}
});

const eventBars = computed(() => {
  if (!props.events_of_the_year) return [];

  const year = props.year;
  const startOfYear = new Date(year, 0, 1).getTime();
  const endOfYear = new Date(year + 1, 0, 1).getTime();
  const yearDuration = endOfYear - startOfYear;

  return props.events_of_the_year.map((event) => {
    const [sy, sm, sd] = event.date_start;
    const [ey, em, ed] = event.date_end;

    // Assuming 1-based months in input, converting to 0-based for Date
    const startDate = new Date(sy, sm - 1, sd);
    // Inclusive end date: set to the start of the next day
    const endDate = new Date(ey, em - 1, ed + 1);

    const startPos = ((startDate.getTime() - startOfYear) / yearDuration) * 100;
    const endPos = ((endDate.getTime() - startOfYear) / yearDuration) * 100;
    const width = endPos - startPos;

    return {
      style: {
        left: `${startPos}%`,
        width: `${width}%`,
      },
    };
  });
});

const monthSeparators = computed(() => {
  const year = props.year;
  const startOfYear = new Date(year, 0, 1).getTime();
  const endOfYear = new Date(year + 1, 0, 1).getTime();
  const yearDuration = endOfYear - startOfYear;

  const separators = [];
  // 0 to 12 covers Jan 1 to Jan 1 next year (13 points)
  for (let i = 0; i <= 12; i++) {
    const date = new Date(year, i, 1);
    const position = ((date.getTime() - startOfYear) / yearDuration) * 100;
    
    let name = "";
    if (i < 12) {
        name = date.toLocaleString('default', { month: 'short' });
    }

    separators.push({
      position,
      name,
      date
    });
  }
  return separators;
});
</script>

<style scoped>
:root {
  --event-lightness: 40%;
  --event-active-saturation: 70%;
  --event-inactive-saturation: 30%;
}

.timeline-wrapper {
  display: flex;
  align-items: center;
  width: 95%;
  height: 3em;
  margin: 0 auto;
}

.year-label {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  font-weight: bold;
  margin-right: 1em;
  font-size: 1.2em;
  color: #555;
}

.timeline-container {
  position: relative;
  flex-grow: 1;
  height: 100%;
  display: flex;
  align-items: center;
}

.timeline-line {
  position: absolute;
  width: 100%;
  height: 2px;
  background-color: #333;
  top: 50%;
  transform: translateY(-50%);
}

.month-marker {
  position: absolute;
  top: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.month-dot {
  width: 6px;
  height: 6px;
  background-color: #555;
  border-radius: 50%;
  transform: translateY(-50%);
}

.month-label {
  margin-top: 0px;
  font-size: 0.75em;
  color: #666;
  white-space: nowrap;
}
.event-bar {
  position: absolute;
  top: 50%;
  height: 10px;
  background-color: rgba(100, 149, 237, 0.7); /* CornflowerBlue with opacity */
  border-radius: 5px;
  transform: translateY(-50%);
  z-index: 1; /* Ensure it's above the line but maybe below dots if desired, or above dots? */
}</style>
