<!--============================================================ ...
    An Event group
... ============================================================ -->

<template>
  <div class="eg-div">
    <a class="eg-title">{{ headerTitles }}</a>

    <table>
      <thead>
        <tr><th>Event</th>      <th>Date</th></tr>
      </thead>
      <tbody>
        <tr v-for="(val, i) in descriptionEvents" :key="i">
            <th>{{val.dates}}</th><th>{{val.name}}</th>
        </tr>
      </tbody>
    </table>
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
      return this.event_group_db["aliases"].join(" / ")
    },
    descriptionEvents() {
      console.log("A")
      if (!this.event_group_db.hasOwnProperty("events")) {
        return [];
      }
      
      let events = this.event_group_db["events"];
      let descs = [];

      console.log("C")
      events.forEach(event => {
        let event_desc = { dates: "", name: "" };
        if ("dates" in event) {
          event_desc.dates = event.dates;
        }
        if ("aliases" in event && event["aliases"].length > 0) {
          event_desc.name = event["aliases"][0];
        }
        descs.push(event_desc);
      });
      console.log("D")

      return descs
    }

  }
};
</script>

<style scoped>
  @import '@/assets/common.css';

  .eg-div {
    margin: 1em;
    /* border: 2px solid var(--greyish-soft); */
    background-color: var(--greyish-dark);
    width: auto;
  }

  .eg-title {
    margin: 1em;
    font-size: x-large;
    color: var(--green-mild);
    font-family: "Segoe UI";
    font-weight: 700;
  }

  table {
    width: auto;
    margin: 1em;
    font-size: 18px;
    font-family: Arial, sans-serif;
    box-shadow: 0 0 20px rgba(59, 57, 57, 0.15);
    border: 3px solid var(--green-dark);
    border-radius: 5px;
    overflow: hidden;
    text-align: left;
    border-collapse: separate; 
    border-spacing: 0;
  }

  thead tr {
    background-color: var(--green-dark);
    color: var(--grey-vibrant);
    text-align: left;
  }

  th {
    padding: 0 0.3em;
    text-align: left;
  }

  tr:nth-child(even) {
    background-color: var(--grey-dark);
  }
</style>
