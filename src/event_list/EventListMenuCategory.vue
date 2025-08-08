<!--============================================================ ...
    An Event group for the menu
... ============================================================ -->

<template>
  <div>
    <!-- Category header. Only if name!='' (root)-->
    <a class="em-categ-name" v-if="ec_name" :href="`#${ec_name}`">
      {{ ec_name }}
    </a>

    <div class="em-eventgroups-div">
      <div v-for="(val, i) in eventGroups" :key="i"> <!-- Event groups for this category -->
         <a class="em-eventgroup-a" :href="`#${i}`">{{ val['aliases'][0] }}</a>
      </div>

      <!-- Sub categories -->
      <div v-for="(sub_categ_desc, i) in subCategories" :key="i">
        <EventListMenuCategory
          v-if="sub_categ_desc.index != undefined"
          :event_list_index="sub_categ_desc.index"
          :ec_name="sub_categ_desc.name"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  event_list_index: Object,
  ec_name: String,
});

const eventGroups = computed(() => {
  if (!props.event_list_index.hasOwnProperty("@databases") || !props.event_list_index["@databases"]) {return [];}
  
  return props.event_list_index["@databases"];
});

const subCategories = computed(() => {
  if (props.event_list_index == undefined) {
    return [];
  }
  /* dict of indexes for the children groups {categ_name: categ_index}*/
  let out_list = [];

  for (const key in props.event_list_index) {
    if (["@databases", "@count"].includes(key)) {
      continue;
    } // Exclude reserved

    let sub_categ_description = {
      // Make description dict
      index: props.event_list_index[key],
      name: key,
    };

    out_list.push(sub_categ_description);
  }

  return out_list;
});

</script>

<style scoped>
@import "@/assets/common.css";

a.em-categ-name {
  padding-left: 0.5em;
  font-weight: 700;
  color: var(--purple-dark)
}

.em-eventgroups-div {
  padding-left: 1em;
}

a.em-eventgroup-a {
  color: var(--green-soft)
}
</style>
