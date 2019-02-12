<template>
  <div class="schema_props">
    <div class="cube_components">
      <button @click="selectedComponent = 'app-cube'">Cube</button>
      <button @click="selectedComponent = 'app-dimensions'">Dimensions</button>
      <button @click="selectedComponent = 'app-facts'">Facts</button>
      <keep-alive>
        <component :is="selectedComponent"> </component>
      </keep-alive>
    </div>
  </div>
</template>

<script>
import cubeDetails from "./the-cube-details";
import cubeDimensions from "./the-cube-dimensions";
import cubeFacts from "./the-cube-facts";

export default {
  data: function() {
    return {
      selectedComponent: "appCube",
    };
  },
  components: {
    "app-cube": cubeDetails,
    "app-dimensions": cubeDimensions,
    "app-facts": cubeFacts,
  },
};
</script>

<style scoped>
.schema_props {
  position: relative;
  float: left;
  top: 30px;
  left: 25px;
  width: 800px;
  height: 480px;
  border: 1px solid #98a6ad;
  padding: 10px;
}

.cube_components {
  position: relative;
  float: top;
  padding: 5px;
  width: 100%;
  height: 40px;
  border: 1px solid #98a6ad;
}

button {
  margin-left: 5px;
}
</style>
