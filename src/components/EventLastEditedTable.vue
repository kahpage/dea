<template>
  <div class="last-edited-card">
    <h3 class="last-edited-title">{{ title }}</h3>
    <div class="last-edited-body">
      <table v-if="rows.length" class="last-edited-table">
        <colgroup>
          <col class="col-date" />
          <col class="col-name" />
          <col class="col-timeline" />
        </colgroup>
        <thead>
          <tr>
            <th class="header-cell">Date</th>
            <th class="header-cell">Name</th>
            <th class="header-cell">Last edited</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.name">
            <td class="row-date">{{ row.dates || "" }}</td>
            <td class="row-name">{{ row.name }}</td>
            <td class="timeline-cell">
              <div
                class="timeline-row"
                :class="{ 'row-missing': row.isMissing }"
              >
                <div class="timeline-line"></div>
                <div
                  v-for="marker in yearMarkers"
                  :key="row.name + '-' + marker.year"
                  class="year-marker"
                  :style="{ left: marker.position + '%' }"
                >
                  <div class="year-dot"></div>
                  <div class="year-label">{{ marker.year }}</div>
                </div>
                <div
                  v-if="row.lastEditedDate"
                  class="event-dot-wrapper"
                  :style="{ left: row.lastEditedPct + '%' }"
                  title="Last edited"
                  aria-label="Last edited"
                >
                  <div class="event-dot"></div>
                  <div class="event-tooltip">{{ row.lastEditedLabel }}</div>
                </div>
                <div
                  v-else
                  class="na-wrapper"
                  title="The last_edited parameter should be set in the database. Please update the database accordingly"
                  aria-label="Missing last_edited: update database"
                >
                  <div class="event-tooltip">
                    Last edited: N/A (not specified)
                  </div>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">No events found.</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  events: {
    type: Object,
    default: () => ({}),
  },
  title: {
    type: String,
    default: "Last edited",
  },
});

function parseLastEdited(value) {
  if (!value) return null;
  const text = String(value);
  const fullDate = [...text.matchAll(/(\d{4})[.\-/](\d{2})[.\-/](\d{2})/g)];
  if (fullDate.length > 0) {
    const last = fullDate[fullDate.length - 1];
    const year = Number(last[1]);
    const month = Number(last[2]);
    const day = Number(last[3]);
    return new Date(year, month - 1, day);
  }
  const yearOnly = [...text.matchAll(/(\d{4})/g)];
  if (yearOnly.length > 0) {
    const last = yearOnly[yearOnly.length - 1];
    const year = Number(last[1]);
    return new Date(year, 0, 1);
  }
  return null;
}

function parseEventDate(value) {
  if (!value) return null;
  const text = String(value);
  const rangeMatches = [...text.matchAll(/(\d{4})\.(\d{2})\.(\d{2})\s*-\s*(\d{4})\.(\d{2})\.(\d{2})/g)];
  if (rangeMatches.length > 0) {
    const last = rangeMatches[rangeMatches.length - 1];
    const year = Number(last[1]);
    const month = Number(last[2]);
    const day = Number(last[3]);
    return new Date(year, month - 1, day);
  }
  const singleMatches = [...text.matchAll(/(\d{4})\.(\d{2})\.(\d{2})/g)];
  if (singleMatches.length > 0) {
    const last = singleMatches[singleMatches.length - 1];
    const year = Number(last[1]);
    const month = Number(last[2]);
    const day = Number(last[3]);
    return new Date(year, month - 1, day);
  }
  return null;
}

function formatDateLabel(date) {
  if (!date) return "";
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `Last edited: ${year}.${month}.${day}`;
}


const range = computed(() => {
  const nowYear = new Date().getFullYear();
  let minYear = nowYear;
  let maxYearExclusive = nowYear + 1;

  const years = Object.values(props.events || {})
    .map((entry) => parseLastEdited(entry?.last_edited))
    .filter(Boolean)
    .map((date) => date.getFullYear());

  if (years.length > 0) {
    const actualMin = Math.min(...years);
    const actualMax = Math.max(...years);
    minYear = Math.min(minYear, actualMin);
    maxYearExclusive = Math.max(maxYearExclusive, actualMax + 1, nowYear + 1);
  }

  if (maxYearExclusive <= minYear) {
    maxYearExclusive = minYear + 1;
  }

  const start = new Date(minYear, 0, 1);
  const end = new Date(maxYearExclusive, 0, 1);
  const duration = end.getTime() - start.getTime();

  return {
    minYear,
    maxYearExclusive,
    start,
    end,
    duration: duration <= 0 ? 1 : duration,
  };
});

const rows = computed(() => {
  const entries = Object.entries(props.events || {}).map(([name, data]) => {
    const record = data || {};
    const index = Number.isFinite(record.index) ? record.index : null;
    const eventDate = parseEventDate(record.dates);
    const eventDateMs = eventDate ? eventDate.getTime() : Number.POSITIVE_INFINITY;
    const lastEditedDate = parseLastEdited(record.last_edited);
    const lastEditedLabel = record.last_edited
      ? `Last edited: ${String(record.last_edited)}`
      : formatDateLabel(lastEditedDate);
    let lastEditedPct = 0;
    if (lastEditedDate) {
      const ms = lastEditedDate.getTime() - range.value.start.getTime();
      lastEditedPct = Math.max(0, Math.min(100, (ms / range.value.duration) * 100));
    }
    return {
      name: String(name),
      dates: record.dates ?? "",
      index,
      eventDateMs,
      lastEditedDate,
      lastEditedPct,
      isMissing: !lastEditedDate,
      lastEditedLabel,
    };
  });

  entries.sort((a, b) => {
    if (a.eventDateMs !== b.eventDateMs) {
      return a.eventDateMs - b.eventDateMs;
    }
    return a.name.localeCompare(b.name);
  });

  return entries;
});

const yearMarkers = computed(() => {
  const markers = [];
  const start = range.value.start.getTime();
  const duration = range.value.duration;
  for (let year = range.value.minYear; year <= range.value.maxYearExclusive; year += 1) {
    const date = new Date(year, 0, 1);
    const position = ((date.getTime() - start) / duration) * 100;
    markers.push({
      year,
      position: Math.max(0, Math.min(100, position)),
    });
  }
  return markers;
});
</script>

<style scoped>
.last-edited-card {
  margin-top: 0.6em;
  border: 5px solid var(--greyish-soft);
  background-color: var(--greyish-dark);
  border-radius: 5px;
  overflow: hidden;
}

.last-edited-title {
  margin: 0;
  padding: 0.2em;
  text-align: center;
  background-color: var(--greyish-soft);
}

.last-edited-body {
  padding: 0.6em;
  overflow-x: auto;
  box-sizing: border-box;
}

.last-edited-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
  color: var(--grey-light);
}

.col-date {
  width: 1%;
}

.col-name {
  width: 1%;
}

.col-timeline {
  width: auto;
}

.header-cell {
  text-align: left;
  color: var(--grey-vibrant);
  font-weight: 700;
  padding: 0.2em 0.4em;
  border-bottom: 1px solid var(--greyish-soft);
}

.last-edited-table tbody tr:nth-child(even) {
  background-color: var(--grey-dark);
}

.row-date,
.row-name {
  padding: 0.2em 0.4em;
  vertical-align: middle;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-date {
  color: var(--grey-mild);
  font-size: 0.9em;
}

.row-name {
  font-weight: 600;
  color: var(--grey-light);
}

.timeline-cell {
  min-width: 10em;
  padding: 0.2em 0.4em;
  vertical-align: top;
}

.timeline-row {
  position: relative;
  height: 2.2em;
  display: flex;
  align-items: center;
  overflow: visible;
}

.timeline-line {
  position: absolute;
  width: 100%;
  height: 2px;
  background-color: #333;
  top: 50%;
  transform: translateY(-50%);
}

.timeline-row.row-missing .timeline-line {
  background-color: var(--scarlet-vibrant);
}

.year-marker {
  position: absolute;
  top: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.year-dot {
  width: 6px;
  height: 6px;
  background-color: #555;
  border-radius: 50%;
  transform: translateY(-50%);
}

.year-label {
  margin-top: 0px;
  font-size: 0.75em;
  color: #666;
  white-space: nowrap;
}

.event-dot-wrapper {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
}

.event-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--scarlet-soft);
  border: 2px solid var(--greyish-dark);
}

.event-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: #ffffff;
  padding: 0.2em 0.4em;
  border-radius: 0.3em;
  font-size: 0.75em;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  margin-bottom: 0.35em;
  transition: opacity 120ms ease-in-out;
}

.event-dot-wrapper:hover .event-tooltip {
  opacity: 1;
  visibility: visible;
}

.timeline-row:hover .event-tooltip {
  opacity: 1;
  visibility: visible;
}

.na-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
}


.na {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  color: var(--scarlet-vibrant);
  font-weight: 700;
  font-size: 0.8em;
}

.empty {
  color: var(--grey-mild);
  font-style: italic;
}
</style>
