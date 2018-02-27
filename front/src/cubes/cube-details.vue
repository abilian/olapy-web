<template>
  <div class="cube_details">
    <label>
      Cube Name :
      <input type="text" :value="currentCube">
    </label>
    <!--<button @click="updateCubeName()"> update cube</button>-->
  </div>
</template>

<script>
import { eventBus } from "../main.js";

export default {
  data: function() {
    return {
      currentCube: "",
    };
  },
  created() {
    eventBus.$on("queriedCube", currentCube => {
      this.currentCube = currentCube;
    });
  },
};
</script>

<style scoped>

</style>
