<template>

  <div class="schema_options">
    <button id="show-modal" @click="showModal = true">Add Cube</button>
    <addCube v-if="showModal" @close="showModal = false">
    </addCube>

  </div>

</template>

<script>
  import addCube from './add_cube/add-cube.vue';

  export default {
    data: function () {
      return {
        showModal: false
      }

    },
    components: {
      addCube: addCube
    }
  }
</script>

<style scoped>

  .schema_options {
    position: relative;
    float: left;
    top: 20px;
    left: 2%;
    width: 180px;
    border: 1px solid #98a6ad;
  }

</style>
