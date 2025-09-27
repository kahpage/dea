<!--============================================================ ...
     Toggle switch component
... ============================================================ -->

<template>
  <label
    class="switch"
    :id="id"
    :title="switch_title"
  >
  <input :id="id" type="checkbox" v-model="innerValue" />
    <span class="slider round"></span>
  </label>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  toggle_value: {  // v-model value to toggle
    type: Boolean,
    required: true,
  },
  id: { // optional id for the label, used for external linking
    type: String,
    required: false,
    default: null,
  },
  titleFunc: { // title function: receives current boolean and returns string
    type: Function,
    required: false,
    default: (state) => "Switch is " + (state ? 'Enabled' : 'Disabled'),
  },
});

// Link internal and external state
const emit = defineEmits(['update:toggle_value']);
const innerValue = computed({
  get: () => props.toggle_value,
  set: (v) => emit('update:toggle_value', v),
});

const switch_title = computed(() => props.titleFunc(innerValue.value));
</script>

<style scoped>
@import "@/assets/common.css";

.toggle {
  padding: 0.5em 0;
}
</style>
