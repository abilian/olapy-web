<template>
  <div class="schema_box">
    <div class="schema_box_container" v-for="cube in cubesNames">
      <input type="button" :value="cube" @click="changeCurrentCube(cube)"><br>
    </div>

  </div>
</template>

<script>
import { eventBus } from "../main.js";

export default {
  data: function() {
    return {
      cubesNames: [],
    };
  },
  methods: {
    getCubes: function() {
      this.$http
        .get("cubes")
        .then(response => {
          return response.json();
        })
        .then(data => {
          for (let key in data) {
            this.cubesNames.push(data[key]);
          }
        });
    },
    changeCurrentCube(cube) {
      eventBus.queriedCube(cube);
    },
  },
  created() {
    this.getCubes();
  },
};
</script>

<style scoped>
.schema_box {
  position: relative;
  float: left;
  top: 30px;
  left: 10px;
  width: 195px;
  height: 480px;
  border: 1px solid #98a6ad;
}

.schema_box_container {
  margin-left: 4px;
  margin-top: 10px;
}
</style>
