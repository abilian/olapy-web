<template>
  <div>
    <h3>dimensions</h3>
    <div v-for="dimension in dimensions">
      <label>
        <input type="text" :name="dimension" :value="dimension">
      </label>
    </div>
  </div>
</template>

<script>
import { eventBus } from "../main.js";

export default {
  name: "cube-dimensions",
  data: function() {
    return {
      currentCube: "",
      dimensions: [],
    };
  },
  methods: {
    getCubeDimensions: function(currentCube) {
      //if errors or cube constrcution probs don't show dimensions
      this.dimensions = [];
      let url = "cubes/" + currentCube + "/dimensions";
      this.$http
        .get(url)
        .then(response => {
          return response.json();
        })
        .then(data => {
          const resultArray = [];
          for (let key in data) {
            resultArray.push(data[key]);
          }
          this.dimensions = resultArray;
        });
    },
  },
  created() {
    eventBus.$on("queriedCube", currentCube => {
      this.currentCube = currentCube;
      this.getCubeDimensions(currentCube);
    });
  },
};
</script>

<style scoped>

</style>
