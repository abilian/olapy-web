<template>
  <div class="cube_details">
    <label>
      Cube Name :
      <input type="text" :value="cubeName">
    </label>

    <button @click="updateCubeName()"> update cube</button>
  </div>
</template>

<script>
  export default {
    name: "cube-details",
    data: function () {
      return {
        cubeName: "MyCube"
      };
    },
    //todo update with api
    methods: {
      updateCubeName: function () {
        this.cubeName = "to_update_late"
      }
    }
  }
</script>

<style scoped>


</style>
