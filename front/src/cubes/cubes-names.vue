<template>
  <div class="schema_box">

    <div class="schema_box_container" v-for="cube in cubesNames">
      <input type="button" :value="cube"><br>
    </div>

  </div>


</template>

<script>
  export default {
    data: function () {
      return {
        //todo method rest api get cubes_names
        cubesNames: ['cube1', 'cube2', 'cube3'],
      };
    },

  }
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
    margin-top: 10px
  }

</style>
