<template>
  <div class="timeline-wrapper">
    <div class="year-label">{{ year }}</div>
    <div class="timeline-container" ref="timelineContainer">
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
        class="event-wrapper"
        :style="event.wrapperStyle"
        @mouseenter="hoveredEventIndex = index"
        @mouseleave="hoveredEventIndex = null"
      >
        <a :href="event.link" class="event-bar" :style="event.barStyle"></a>
        <div
          v-if="hoveredEventIndex === index"
          class="event-tooltip"
          ref="tooltipRef"
          :style="tooltipStyle"
        >
          <table>
            <tbody>
              <tr v-for="overlap in overlappingEvents" :key="overlap.name">
                <td class="tooltip-date">{{ overlap.raw_dates }}</td>
                <td>
                  <a :href="overlap.link" class="tooltip-link">{{
                    overlap.name
                  }}</a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from "vue";
import { useElementBounding } from "@vueuse/core";

const props = defineProps({
  year: {
    type: Number,
    default: new Date().getFullYear()
  },
  events_of_the_year: Array, // List of events of the year {name: event_name,raw_dates: raw_dates,date_start: date_start,date_end: date_end,was_held: was_held,ar_path: event_group_ar_path,hue: hue_event_group}
});

const timelineContainer = ref(null);
const tooltipRef = ref(null);
const { width: containerWidth } = useElementBounding(timelineContainer);
const hoveredEventIndex = ref(null);
const tooltipStyle = ref({});

watch(hoveredEventIndex, async (newIndex) => {
  if (newIndex !== null) {
    await nextTick();
    const tooltipEl = Array.isArray(tooltipRef.value) ? tooltipRef.value[0] : tooltipRef.value;
    
    if (tooltipEl && timelineContainer.value) {
      const tooltipRect = tooltipEl.getBoundingClientRect();
      const containerRect = timelineContainer.value.getBoundingClientRect();
      
      let left = "50%";
      let transform = "translateX(-50%)";

      // Check left overflow
      if (tooltipRect.left < containerRect.left) {
        left = "0";
        transform = "translateX(0)";
      }
      // Check right overflow
      else if (tooltipRect.right > containerRect.right) {
        left = "auto";
        transform = "translateX(0)";
        // We can't easily set right: 0 because it's positioned relative to the event wrapper
        // Instead, we can calculate the offset needed
        const overflow = tooltipRect.right - containerRect.right;
        transform = `translateX(calc(-50% - ${overflow}px))`;
      }

      tooltipStyle.value = {
        left,
        transform
      };
    }
  } else {
    tooltipStyle.value = {};
  }
});

const eventBars = computed(() => {
  if (!props.events_of_the_year) return [];

  const year = props.year;
  const startOfYear = new Date(year, 0, 1).getTime();
  const endOfYear = new Date(year + 1, 0, 1).getTime();
  const yearDuration = endOfYear - startOfYear;

  return props.events_of_the_year
    .map((event) => {
      const [sy, sm, sd] = event.date_start;
      const [ey, em, ed] = event.date_end;

      // Assuming 1-based months in input, converting to 0-based for Date
      const startDate = new Date(sy, sm - 1, sd);
      // Inclusive end date: set to the start of the next day
      const endDate = new Date(ey, em - 1, ed + 1);

      const startPos = ((startDate.getTime() - startOfYear) / yearDuration) * 100;
      const endPos = ((endDate.getTime() - startOfYear) / yearDuration) * 100;
      const width = endPos - startPos;

      const saturation = event.was_held
        ? "var(--event-active-saturation)"
        : "var(--event-inactive-saturation)";
      const backgroundColor = `hsl(${event.hue}, ${saturation}, var(--event-lightness))`;
      const link =
        event.ar_path && Array.isArray(event.ar_path)
          ? "/dea/event_detail/#/" + event.ar_path.join("/") + "/" + event.name
          : "#";

      return {
        name: event.name,
        raw_dates: event.raw_dates,
        link,
        startTime: startDate.getTime(),
        endTime: endDate.getTime(),
        startPct: startPos,
        widthPct: width,
        wrapperStyle: {
          left: `${startPos}%`,
          width: `${width}%`,
          minWidth: "10px",
        },
        barStyle: {
          backgroundColor,
        },
      };
    });
});

const overlappingEvents = computed(() => {
  if (hoveredEventIndex.value === null) return [];
  const hovered = eventBars.value[hoveredEventIndex.value];
  if (!hovered) return [];

  const getRange = (event) => {
    const leftPx = (event.startPct / 100) * containerWidth.value;
    let widthPx = (event.widthPct / 100) * containerWidth.value;
    if (widthPx < 10) widthPx = 10;
    return { start: leftPx, end: leftPx + widthPx };
  };

  const hoveredRange = getRange(hovered);

  return eventBars.value.filter((event) => {
    const range = getRange(event);
    return (
      hoveredRange.start < range.end && hoveredRange.end > range.start
    );
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
.timeline-wrapper {
  --event-lightness: 40%;
  --event-active-saturation: 70%;
  --event-inactive-saturation: 30%;

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
.event-wrapper {
  position: absolute;
  top: 50%;
  height: 10px;
  transform: translateY(-50%);
  z-index: 1;
}

.event-bar {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 5px;
  cursor: pointer;
}

.event-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  white-space: nowrap;
  z-index: 10;
  margin-bottom: 5px;
  cursor: default;
}

.event-tooltip::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  height: 5px;
}

.event-tooltip table {
  border-collapse: collapse;
}

.event-tooltip td {
  padding: 2px 5px;
  vertical-align: top;
}

.tooltip-date {
  color: #ccc;
  font-size: 0.9em;
  white-space: nowrap;
  text-align: right;
  padding-right: 10px;
}

.tooltip-link {
  color: white;
  text-decoration: none;
  display: block;
}

.tooltip-link:hover {
  text-decoration: underline;
}
</style>
