<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              <div class="table-responsive" v-html="resultCube"></div>
            </slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">
              <button class="btn btn-default" @click="$emit('close', false)">
                close
              </button>
              <button class="btn btn-success" @click="confirmCustomCube()">
                Next
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import axios from "axios";
import { eventModalBus } from "../base-add-cube.vue";

export default {
  props: {
    cubeName: String,
    factsTable: String,
    tablesAndColumnsResult: Object,
    chosenMeasures: Array,
    SavedColumns: Array,
    dbConfig: String,
  },

  data: function () {
    return {
      resultCube: "",
    };
  },

  created() {
    const data = {
      cubeName: this.cubeName,
      factsTable: this.factsTable,
      tablesAndColumnsResult: this.tablesAndColumnsResult,
      columnsPerDimension: this.SavedColumns,
      measures: this.chosenMeasures,
      dbConfig: this.dbConfig,
    };
    axios
      .post("/api/cubes/construct_custom_cube", data)
      .then((response) => {
        this.resultCube = response.data;
      })
      .catch(() => {
        this.$notify({
          group: "user",
          title: "unable to construct cube, check your tables relations",
          type: "error",
        });
        eventModalBus.modalToShow("makeRelations");
      });
  },

  methods: {
    confirmCustomCube() {
      // this.$emit('tablesAndColumnsResult', this.tablesAndColumnsResult);
      const data = {
        cubeName: this.cubeName,
        customCube: true,
      };
      axios.post("/api/cubes/confirm_cube", data).then((response) => {
        eventModalBus.modalToShow("success");
        return response.data;
      });
    },
  },
};
</script>

<style scoped>
.modal-container {
  width: 900px;
}
</style>
