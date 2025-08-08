<!--============================================================ ...
     Event List page
... ============================================================ -->

<script setup>
import EventCategory from "@/components/EventCategory.vue";
import EventListMenuCategory from "./EventListMenuCategory.vue";
import Navigation from "@/components/Navigation.vue"

import event_list_index from "@/assets/static_databases/event_list_index.json"; // Static database import

</script>

<template>
  <!-- event_list_index = {{ event_list_index }} -->

  <!-- Title -->
  <head>
    <title>dea | Event List</title>
  </head>

  <div class="el-container">
    <div class="el-content">
      <section id="top"></section>
      <Navigation/>
      <div class="header-title">Event list</div>
      <div class="header">A list of various events in the database.</div>

      <EventCategory
        v-if="event_list_index !== undefined"
        :event_list_index="event_list_index"
        :ec_name="''"
        :ar_path="[]"
      />
    </div>
    <div class="el-menu">
      <a class="el-menu-title" href="#top" title="Go Top">▲</a><span class="el-menu-title">Content</span>
      <EventListMenuCategory
        v-if="event_list_index !== undefined"
        :event_list_index="event_list_index"
        :ec_name="''"
      ></EventListMenuCategory>
    </div>
  </div>
</template>

<style>
@import "@/assets/common.css";

.el-container {
  display: flex;
  flex-direction: row;
  height: 100vh; 
  width: 100%; 
}

.el-content {
  flex: 1; 
  overflow-y: auto; 
  padding: 0;
  box-sizing: border-box;
}

.el-menu {
  width: 25%;
  background-color: var(--greyish-mild);
  padding-left: 0.5em;
  padding-top: 1em;
  height: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}

.el-menu-title {
  font-size: x-large;
  font-weight: 700;
  color: var(--purple-deep);
}
a.el-menu-title {
  font-size: medium;
  font-weight: 700;
  color: var(--purple-deep);
}
</style>
