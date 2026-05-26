<script setup>
import { computed, ref, watch, onBeforeUnmount } from "vue";
import { useVirtualList } from "@vueuse/core";
import FilterEntry from "@/components/FilterEntry.vue";

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  searchTextGetter: {
    type: Function,
    default: (item) => {
      if (item === null || item === undefined) return "";
      if (typeof item === "string") return item;
      try {
        return JSON.stringify(item);
      } catch (e) {
        return String(item);
      }
    },
  },
  itemHeight: {
    type: Number,
    default: 22,
  },
  debounceMs: {
    type: Number,
    default: 0,
  },
  searchPlaceholder: {
    type: String,
    default: "Keywords",
  },
  showRegexToggle: {
    type: Boolean,
    default: true,
  },
  regexLabel: {
    type: String,
    default: "Use Regex ?",
  },
  resultsLabel: {
    type: String,
    default: "results",
  },
  regexEmptyReturnsAll: {
    type: Boolean,
    default: false,
  },
  contourColor: {
    type: String,
    default: "var(--grey-dark)",
  },
  rowsColor: {
    type: String,
    default: "var(--grey-dark)",
  },
});

const filters = ref([]);

const active_filters = computed(() =>
  filters.value.filter((filter) => {
    const query = (filter.query || "").trim();
    return query.length > 0 || filter.useRegex;
  })
);

const filtered_indexes = computed(() => {
  if (!Array.isArray(props.items) || props.items.length === 0) {
    return [];
  }

  const active = active_filters.value;
  if (active.length === 0) {
    return props.items.map((_, index) => index);
  }

  let current_indexes = props.items.map((_, index) => index);
  for (const filter of active) {
    const raw_query = (filter.query || "").trim();
    if (!raw_query && !filter.useRegex) {
      continue;
    }

    if (filter.useRegex) {
      if (!raw_query) {
        if (!props.regexEmptyReturnsAll) return [];
        continue;
      }
      let re = null;
      try {
        re = new RegExp(raw_query, "i");
      } catch (e) {
        return [];
      }
      current_indexes = current_indexes.filter((index) => {
        const text = props.searchTextGetter(props.items[index], index);
        return re.test(text === null || text === undefined ? "" : String(text));
      });
      continue;
    }

    const lowered_query = raw_query.toLowerCase();
    current_indexes = current_indexes.filter((index) => {
      const text = props.searchTextGetter(props.items[index], index);
      const normalized = text === null || text === undefined ? "" : String(text);
      return normalized.toLowerCase().includes(lowered_query);
    });
  }

  return current_indexes;
});

const filtered_items = computed(() =>
  filtered_indexes.value.map((index) => props.items[index])
);

const { list, containerProps, wrapperProps, scrollTo } = useVirtualList(
  filtered_items,
  {
    itemHeight: props.itemHeight,
  }
);

const root_style = computed(() => ({
  "--svl-contour-color": props.contourColor,
  "--svl-rows-color": props.rowsColor,
  "--svl-item-height": `${props.itemHeight}px`,
}));

const viewport_props = computed(() => ({
  ...containerProps,
  style: {
    ...(containerProps.style || {}),
    minHeight: "0",
    overscrollBehavior: "contain",
  },
}));

const wrapper_props = computed(() => {
  const base = wrapperProps.value || {};
  return {
    ...base,
    style: {
      ...(base.style || {}),
      width: "100%",
      minHeight: "0",
    },
  };
});

function getRowStyle(index, start) {
  return {
    height: `${props.itemHeight}px`,
    lineHeight: "var(--svl-item-height)",
    boxSizing: "border-box",
    backgroundColor:
      index % 2 === 0
        ? "var(--svl-rows-color)"
        : "color-mix(in srgb, var(--svl-rows-color) 82%, black)",
    color: "var(--grey-light)",
  };
}

const visible_list = computed(() =>
  list.value.map((vitem) => ({
    ...vitem,
    rowProps: {
      class: [
        "searchable-virtual-list__row",
        vitem.index % 2 === 0
          ? "searchable-virtual-list__row-even"
          : "searchable-virtual-list__row-odd",
      ],
      style: getRowStyle(vitem.index, vitem.start),
    },
  }))
);

function addFilter() {
  filters.value.push({
    input: "",
    query: "",
    useRegex: false,
    debounceTimer: null,
  });
}

function removeFilter(index) {
  const filter = filters.value[index];
  if (filter?.debounceTimer) {
    clearTimeout(filter.debounceTimer);
  }
  filters.value.splice(index, 1);
  scrollTo(0);
}

function commitFilter(index, value) {
  const filter = filters.value[index];
  if (!filter) return;
  filter.query = value;
  scrollTo(0);
}

function onFilterInput(index, value) {
  const filter = filters.value[index];
  if (!filter) return;
  filter.input = value;

  if (filter.debounceTimer) {
    clearTimeout(filter.debounceTimer);
    filter.debounceTimer = null;
  }

  if (props.debounceMs > 0) {
    filter.debounceTimer = setTimeout(() => {
      commitFilter(index, value);
      filter.debounceTimer = null;
    }, props.debounceMs);
    return;
  }

  commitFilter(index, value);
}

function onFilterRegex(index, value) {
  const filter = filters.value[index];
  if (!filter) return;
  filter.useRegex = value;
  scrollTo(0);
}

onBeforeUnmount(() => {
  for (const filter of filters.value) {
    if (filter.debounceTimer) {
      clearTimeout(filter.debounceTimer);
      filter.debounceTimer = null;
    }
  }
});
</script>

<template>
  <div class="searchable-virtual-list" :style="root_style">
    <div class="searchable-virtual-list__filters">
      <div class="searchable-virtual-list__filter-sidebar">
        <div class="searchable-virtual-list__filter-actions">
          <button
            class="searchable-virtual-list__filter-button"
            @click="addFilter"
            title="Add filtering criterium"
          >
            Add filter
          </button>
        </div>

        <div class="searchable-virtual-list__results">
          ({{ filtered_items.length }} {{ resultsLabel }})
        </div>
      </div>

      <div class="searchable-virtual-list__filter-list">
        <div
          v-for="(filter, index) in filters"
          :key="index"
          class="searchable-virtual-list__filter-row"
        >
          <FilterEntry
            :model-value="filter.input"
            :use-regex="filter.useRegex"
            :placeholder="searchPlaceholder"
            :regex-label="regexLabel"
            @update:modelValue="(value) => onFilterInput(index, value)"
            @update:useRegex="(value) => onFilterRegex(index, value)"
          />
          <button
            class="searchable-virtual-list__filter-remove"
            @click="removeFilter(index)"
            aria-label="Remove filter"
            title="Remove filter"
          >
            ×
          </button>
        </div>
      </div>
    </div>

    <slot
      name="header"
      :items="filtered_items"
      :filters="filters"
      :scrollTo="scrollTo"
    />

    <div v-bind="viewport_props" class="searchable-virtual-list__viewport">
      <div v-bind="wrapper_props" class="searchable-virtual-list__wrapper">
        <slot
          :list="visible_list"
          :items="filtered_items"
          :filters="filters"
          :scrollTo="scrollTo"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.searchable-virtual-list {
  display: flex;
  flex-direction: column;
  min-height: 0;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  padding-inline: 0.25em;
  background-color: var(--svl-contour-color);
  border: 3px solid var(--svl-contour-color);
  border-radius: 5px;
}

.searchable-virtual-list__filters {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
}

.searchable-virtual-list__filter-sidebar {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 0 0 auto;
}

.searchable-virtual-list__filter-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.searchable-virtual-list__filter-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1 1 28rem;
  min-width: 0;
}

.searchable-virtual-list__filter-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.searchable-virtual-list__filter-button {
  background-color: var(--purple-dark);
  color: var(--grey-vibrant);
  border: none;
  padding: 0.3em 0.6em;
  border-radius: 0.25em;
  cursor: pointer;
  font-weight: 600;
}

.searchable-virtual-list__filter-button:hover {
  filter: brightness(0.95);
}

.searchable-virtual-list__filter-remove {
  background-color: var(--scarlet-vibrant);
  border: none;
  color: var(--grey-light);
  padding: 0.1em 0.2em;
  font-size: 0.85rem;
  line-height: 1;
  min-width: auto;
  min-height: auto;
  border-radius: 0.2em;
  cursor: pointer;
}

.searchable-virtual-list__filter-remove:hover {
  filter: brightness(0.9);
}

.searchable-virtual-list__results {
  font-weight: 600;
}

.searchable-virtual-list__viewport {
  flex: 1 1 auto;
  position: relative;
  box-sizing: border-box;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
}

.searchable-virtual-list__wrapper {
  display: block;
  position: relative;
  width: 100%;
  box-sizing: border-box;
}

.searchable-virtual-list__row {
  color: var(--grey-light);
}

.searchable-virtual-list__row-even {
  background-color: var(--svl-rows-color);
}

.searchable-virtual-list__row-odd {
  background-color: color-mix(in srgb, var(--svl-rows-color) 82%, black);
}
</style>