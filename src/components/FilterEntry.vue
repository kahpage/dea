<script setup>
import ToggleSwitch from "@/components/ToggleSwitch.vue";

defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  useRegex: {
    type: Boolean,
    default: false,
  },
  placeholder: {
    type: String,
    default: "Keywords",
  },
  regexLabel: {
    type: String,
    default: "Use Regex ?",
  },
});

defineEmits(["update:modelValue", "update:useRegex"]);
</script>

<template>
  <div class="filter-entry">
    <div class="filter-entry__regex-group">
      <div class="filter-entry__regex-label">regex</div>
      <ToggleSwitch
        :toggle_value="useRegex"
        :titleFunc="
          (state) => (state ? 'regex search enabled' : 'regex search disabled')
        "
        @update:toggle_value="$emit('update:useRegex', $event)"
      />
    </div>

    <input
      class="filter-entry__input"
      :value="modelValue"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<style scoped>
.filter-entry {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-entry__input {
  min-width: 12rem;
  background-color: var(--grey-vibrant);
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0.4em 0.6em;
  border-radius: 0.25em;
}

.filter-entry__regex-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  font-weight: 700;
}

.filter-entry__regex-label {
  font-size: 0.95rem;
  line-height: 1;
  white-space: nowrap;
}
</style>
