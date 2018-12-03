<template>
  <!-- <div class="schema_props"> -->
  <div>
    <h3>facts and measures</h3>
    <div v-if="facts.table_name">
      <label>
        Facts table name :
        <input type="text" :name="facts.table_name" :value="facts.table_name" />
      </label>
      <hr />
      <span>Measures :</span> <br />
      <div v-for="(measure, index) in facts.measures">
        <label>
          <input type="text" :key="index" :name="measure" :value="measure" />
        </label>
      </div>
      <label>
        <input
          style="margin: 50px 50px"
          type="Button"
          class="btn button-list"
          value="Update"
        />
      </label>
    </div>
  </div>
</template>

<script>
import { eventBus } from "../main.js";

export default {
  name: "cube-facts",
  data: function() {
    return {
      facts: {
        table_name: "",
        measures: [],
      },
    };
  },
  methods: {
    getCubeFacts: function(currentCube) {
      //if errors or cube constrcution probs don't show facts
      this.facts = {};
      let url = "api/cubes/" + currentCube + "/facts";
      this.$http
        .get(url)
        .then(response => {
          return response.json();
        })
        .then(data => {
          this.facts = data;
        });
    },
  },
  created() {
    eventBus.$on("queriedCube", currentCube => {
      this.getCubeFacts(currentCube);
    });
  },
};
</script>

<style scoped></style>
