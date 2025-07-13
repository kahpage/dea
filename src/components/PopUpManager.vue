<!--============================================================ ...
     Pop Up stack manager component
... ============================================================ -->

<template>
  <div class="popup-stack">
    <component
      v-for="(popup, index) in popups"
      :key="index"
      :is="popup.component"
      v-bind="popup.props"
      @close="closePopup(index)"
      :style="{ 'z-index': defaultZIndex + index }"
    />    
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeMount } from 'vue';
const popups = ref([]);
const defaultZIndex = 1000;

function addPopup(component, props) {
  popups.value.push({
    component,
    props: { ...props}
  });
}

function closePopup(index) {
  popups.value.splice(index, 1);
}

function closeTopPopup() {
  if (popups?.value && popups.value.length > 0) {
    popups.value.pop();
  }
}


/* Close when pressing Escape */
function handleKeyDown(event) {
  if (event.key === 'Escape') {closeTopPopup();}
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown); // Add event listener for Escape key
});

onBeforeMount(() => {
  window.removeEventListener('keydown', handleKeyDown); // Cleanup event listener on component unmount
});

defineExpose({
  addPopup,
  closePopup,
  closeTopPopup,
  popups
})
</script>

<style scoped>
@import "@/assets/common.css";

</style>