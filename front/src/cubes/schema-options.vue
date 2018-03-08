<template>

  <div class="schema_options">
    <button id="show-modal" @click="showModal = true">Add Cube</button>
    <add-cube v-if="showModal && modalToShow === 'first'" @newCubeName="newCubeName = $event"
              @close="showModal = $event">
    </add-cube>
    <!--@close="showModal = false"-->

    <config-uploaded-tables v-if="showModal && modalToShow === 'second'" :dbConfig="dbConfig" :cubeName="newCubeName"
                            :cube="cube" @close="showModal = $event">
    </config-uploaded-tables>
    <keep-alive>
      <customize-cube v-if="showModal && modalToShow === 'toConfig'" :cubeName="newCubeName" :cube="cube"
                      @factsTable="factsTable = $event" @chosenTables="chosenTables = $event"
                      @chosenMeasures="chosenMeasures = $event" @selectTableColumns="selectTableColumns = $event"
                      :SavedColumns="SavedColumns" :dbConfig="dbConfig" @SavedColumns="SavedColumns = $event"
                      @close="showModal = $event">
      </customize-cube>
    </keep-alive>
    <select-dim-columns v-if="showModal && modalToShow === 'choseColumns'" @SavedColumns="SavedColumns = $event"
                        :selectTableColumns="selectTableColumns" @close="showModal = $event">
    </select-dim-columns>

    <table-relations v-if="showModal && modalToShow === 'makeRelations'" :factsTable="factsTable"
                     :chosenTables="chosenTables" :chosenMeasures="chosenMeasures" :dbConfig="dbConfig"
                     @tablesAndColumnsResult="tablesAndColumnsResult = $event" @close="showModal = $event">
    </table-relations>
    <custom-cube-result v-if="showModal && modalToShow === 'confirmCustomCube'" :cubeName="newCubeName"
                        :factsTable="factsTable" :chosenMeasures="chosenMeasures"
                        :tablesAndColumnsResult="tablesAndColumnsResult" :dbConfig="dbConfig"
                        :SavedColumns="SavedColumns" @close="showModal = $event">
    </custom-cube-result>
    <added-success v-if="showModal && modalToShow === 'success'" @close="showModal = $event">
    </added-success>
  </div>

</template>

<script>
import addCube from "./add_cube/add-cube.vue";
import configUploadedTables from "./add_cube/config-upladed-tables.vue";
import addedSuccess from "./add_cube/added-success.vue";
import selectDimColumns from "./add_cube/select-dimension-columns";
import customizeCube from "./add_cube/customize-cube";
import tableRelations from "./add_cube/tables-relations";
import customCubeResult from "./add_cube/customCubeResult";

import Vue from "vue";

export const eventModalBus = new Vue({
  methods: {
    modalToShow(modal) {
      this.$emit("modalToShow", modal);
    },
    cubeConstructed(cube) {
      this.$emit("cubeConstructed", cube);
    },
    ConnectionConfig(config) {
      this.$emit("ConnectionConfig", config);
    },
  },
});

export default {
  data: function() {
    return {
      showModal: false,
      modalToShow: "first",
      cube: "",
      dbConfig: "",
    };
  },
  components: {
    addCube: addCube,
    configUploadedTables: configUploadedTables,
    customizeCube: customizeCube,
    selectDimColumns: selectDimColumns,
    tableRelations: tableRelations,
    customCubeResult: customCubeResult,
    addedSuccess: addedSuccess,
  },
  created() {
    eventModalBus.$on("modalToShow", modal => {
      this.modalToShow = modal;
    });
    eventModalBus.$on("cubeConstructed", Cube => {
      this.cube = Cube;
    });
    eventModalBus.$on("ConnectionConfig", config => {
      this.dbConfig = config;
    });
  },
  watch: {
    showModal: function() {
      this.modalToShow = "first";
      this.cube = "";
      this.dbConfig = "";
      this.$http.post("api/cubes/clean_tmp_dir");
    },
  },
};
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
