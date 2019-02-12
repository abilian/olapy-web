<template>
  <div>
    <div class="page-wrapper">
      <div class="row page-titles">
        <div class="col-md-5 align-self-center">
          <button
            id="show-modal"
            @click="showModal = true"
            type="button"
            class="btn btn-primary btn-flat btn-addon m-b-10 m-l-5"
          >
            <i class="ti-plus"></i>Add Cube
          </button>
        </div>
      </div>
    </div>

    <add-cube
      v-if="showModal && modalToShow === 'first'"
      @newCubeName="newCubeName = $event"
      @close="showModal = $event"
    />

    <config-uploaded-tables
      v-if="showModal && modalToShow === 'second'"
      :dbConfig="dbConfig"
      :cubeName="newCubeName"
      :cube="cube"
      @close="showModal = $event"
    />

    <keep-alive>
      <customize-cube
        v-if="showModal && modalToShow === 'toConfig'"
        :cubeName="newCubeName"
        :cube="cube"
        @factsTable="factsTable = $event"
        @chosenTables="chosenTables = $event"
        @chosenMeasures="chosenMeasures = $event"
        @selectTableColumns="selectTableColumns = $event"
        :SavedColumns="SavedColumns"
        :dbConfig="dbConfig"
        @SavedColumns="SavedColumns = $event"
        @close="showModal = $event"
      />
    </keep-alive>

    <select-dim-columns
      v-if="showModal && modalToShow === 'choseColumns'"
      @SavedColumns="SavedColumns = $event"
      :selectTableColumns="selectTableColumns"
      @close="showModal = $event"
    />

    <table-relations
      v-if="showModal && modalToShow === 'makeRelations'"
      :factsTable="factsTable"
      :chosenTables="chosenTables"
      :chosenMeasures="chosenMeasures"
      :dbConfig="dbConfig"
      @tablesAndColumnsResult="tablesAndColumnsResult = $event"
      @close="showModal = $event"
    />

    <custom-cube-result
      v-if="showModal && modalToShow === 'confirmCustomCube'"
      :cubeName="newCubeName"
      :factsTable="factsTable"
      :chosenMeasures="chosenMeasures"
      :tablesAndColumnsResult="tablesAndColumnsResult"
      :dbConfig="dbConfig"
      :SavedColumns="SavedColumns"
      @close="showModal = $event"
    />

    <added-success
      v-if="showModal && modalToShow === 'success'"
      @close="
        showModal = $event;
        $emit('addCubeName', newCubeName);
      "
    />
  </div>
</template>

<script>
const axios = require("axios");
import addCube from "./add_cube/BaseAddCubeButton.vue";
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
      SavedColumns: null,
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
      axios.post("api/cubes/clean_tmp_dir");
    },
  },
};
</script>

<style scoped></style>
