<!--============================================================ ...
     Pop up generic component
... ============================================================ -->

<template>
  <div class="popup-div">
    <div class="popup-background"></div>
    <div class="popup">
      <div class="popup-header">
        <span class="popup-title" >{{ props.title }}</span>
        <button class="popup-close" @click="closePopup">Close</button>
      </div>
      <div class="popup-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: false,
    default: ""
  }
});

const emit = defineEmits(['close']);

function closePopup() {
  emit('close');
}

</script>

<style scoped>
@import "@/assets/common.css";

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--greyish-dark);
  border: 2px solid var(--greyish-soft);
  border-radius: 0.5em;
  pointer-events: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.popup-background {
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  position: fixed;
  background-color: #00000050;
}

.popup-content {
  padding: 0.5em;
  color:
   var(--grey-light);
}

.popup-header {
  background-color: var(--greyish-soft);
  color: var(--grey-light);
  padding: 0.3em;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  box-sizing: border-box;
  position: relative;
}

.popup-title {
  margin: 0 3em;
  width: 100%;
  font-size: 1.2em;
  font-weight: bold;
  text-align: center; /* Ensure title remains centered */
}

.popup-close {
  color: var(--purple-soft);
  background: none;
  position: absolute;
  transform: translateY(-50%);
  padding: 0.3rem;
  border-radius: 0.4em;
  right: 0.2em;
  top: 50%;
  cursor: pointer;
  border: none;
}

.popup-close:hover {
  background-color: var(--green-mild);
  color: var(--grey-vibrant);
}
</style>
