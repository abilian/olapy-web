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
  export default {
    props: ['currentCube'],
    // data: function () {
    //   return {
    //     cubeName: this.currentCube
    //   };
    // }
    // ,
    // //todo update with api
    // methods: {
    //   updateCubeName: function () {
    //     this.cubeName = "to_update_late"
    //   }
    // }
  }
</script>

<style scoped>


</style>
