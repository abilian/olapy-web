<template>

  <div class="schema_options">
    <button id="show-modal" @click="showModal = true">Add Cube</button>
    <addCube v-if="showModal && modalToShow === 'first'">
    </addCube>
    <!--@close="showModal = false"-->
    <configUploadedTables v-if="showModal && modalToShow === 'second'" :cube="cube" >
    </configUploadedTables>
  </div>

</template>

<script>
  import addCube from './add_cube/add-cube.vue';
  import configUploadedTables from './add_cube/config-upladed-tables.vue';
  import Vue from 'vue'

  export const eventModalBus = new Vue({
    methods: {
      modalToShow(modal) {
        this.$emit('modalToShow', modal);
      },
      uploadStatus(status) {
        this.$emit('uploadStatus', status);
      },
      cubeConstructed(cube) {
        this.$emit('cubeConstructed', cube);
      }

    }
  });

  export default {
    data: function () {
      return {
        showModal: false,
        modalToShow: 'first',
        cube: '',

      }

    },
    components: {
      addCube: addCube,
      configUploadedTables: configUploadedTables
    },
    created() {
      eventModalBus.$on('modalToShow', (modal) => {
        this.modalToShow = modal;
      });
      eventModalBus.$on('cubeConstructed', (Cube) => {
        this.cube = Cube;
      });
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
