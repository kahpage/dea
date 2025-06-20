<!--============================================================ ...
    An Event group
... ============================================================ -->

<template>
  <div class="eg-div">
    <a class="eg-title">{{ headerTitles }}</a>

    <a class="eg-title">{{ headerTitles }}</a>
    
  </div>
</template>

<script>
export default {
  name: 'JsonComponent',
  props: {
    event_group_db: {
      type: Object,
      required: true
    }
  },
  computed: {
    headerTitles() {
      return this.event_group_db["aliases"].join(", ")
    }
  }
};
</script>

<style scoped>
  @import '@/assets/common.css';

  .eg-div {
    margin: 1em;
    border: 2px solid #3498db;
  }

  .eg-title {
    font-size: x-large;
    color: var(--green-mild);
    font-family: "Segoe UI";
    font-weight: 700;
  }
</style>
