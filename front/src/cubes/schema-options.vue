<template>

  <div class="schema_options">
    <button id="show-modal" @click="showModal = true">Add Cube</button>
    <addCube v-if="showModal && modalToShow === 'first'" @newCubeName="newCubeName = $event">
    </addCube>
    <!--@close="showModal = false"-->

    <configUploadedTables v-if="showModal && modalToShow === 'second'" :cubeName="newCubeName" :cube="cube">
    </configUploadedTables>
    <keep-alive>
      <customizeCube v-if="showModal && modalToShow === 'toConfig'" :cubeName="newCubeName" :cube="cube"
                     @factsTable="factsTable = $event" @chosenTables="chosenTables = $event"
                     @chosenMeasures="chosenMeasures = $event" @selectTableColumns="selectTableColumns = $event"
                     :SavedColumns="SavedColumns" @SavedColumns="SavedColumns = $event">
      </customizeCube>
    </keep-alive>
    <selectDimColumns v-if="showModal && modalToShow === 'choseColumns'" @SavedColumns="SavedColumns = $event"
                      :selectTableColumns="selectTableColumns">
    </selectDimColumns>

    <tableRelations v-if="showModal && modalToShow === 'makeRelations'" :factsTable="factsTable"
                    :chosenTables="chosenTables" :chosenMeasures="chosenMeasures"
                    @tablesAndColumnsResult="tablesAndColumnsResult = $event">
    </tableRelations>
    <customCubeResult v-if="showModal && modalToShow === 'confirmCustomCube'" :cubeName="newCubeName"
                      :factsTable="factsTable" :chosenMeasures="chosenMeasures"
                      :tablesAndColumnsResult="tablesAndColumnsResult" :SavedColumns="SavedColumns">
    </customCubeResult>
    <addedSuccess v-if="showModal && modalToShow === 'success'" @close="showModal = $event">
    </addedSuccess>
  </div>

</template>

<script>
  import addCube from './add_cube/add-cube.vue';
  import configUploadedTables from './add_cube/config-upladed-tables.vue';
  import addedSuccess from './add_cube/added-success.vue'
  import selectDimColumns from './add_cube/select-dimension-columns'
  import customizeCube from './add_cube/customize-cube'
  import tableRelations from './add_cube/tables-relations'
  import customCubeResult from './add_cube/customCubeResult'

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
      configUploadedTables: configUploadedTables,
      customizeCube: customizeCube,
      selectDimColumns: selectDimColumns,
      tableRelations: tableRelations,
      customCubeResult: customCubeResult,
      addedSuccess: addedSuccess
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
