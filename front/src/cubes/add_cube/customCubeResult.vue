<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              <div class="table-responsive" v-html="resultCube">
              </div>
            </slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">
              <button
                class="modal-default-button"
                @click="confirmCustomCube()">
                Next
              </button>
              <button class="modal-default-button" @click="$emit('close', false)">
                close
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>

</template>

<script>
import { eventModalBus } from "../base-schema-options.vue";

export default {
  props: {
    cubeName: String,
    factsTable: String,
    tablesAndColumnsResult: String,
    chosenMeasures: String,
    SavedColumns: String,
    dbConfig: String,
  },
  data: function() {
    return {
      resultCube: "",
    };
  },
  methods: {
    confirmCustomCube() {
      // this.$emit('tablesAndColumnsResult', this.tablesAndColumnsResult);
      let data = {
        cubeName: this.cubeName,
        customCube: true,
      };
      this.$http.post("api/cubes/confirm_cube", data).then(response => {
        eventModalBus.modalToShow("success");
        return response.json();
      });
    },
  },
  created() {
    let data = {
      cubeName: this.cubeName,
      factsTable: this.factsTable,
      tablesAndColumnsResult: this.tablesAndColumnsResult,
      columnsPerDimension: this.SavedColumns,
      measures: this.chosenMeasures,
      dbConfig: this.dbConfig,
    };
    this.$http
      .post("api/cubes/try_construct_custom_cube", data)
      .then(x => {
        this.resultCube = x.data;
      })
      .catch(err => {
        alert("unable to construct cube, check your tables relations");
        eventModalBus.modalToShow("makeRelations");
      });
  },
};
</script>

<style scoped>
.modal-container {
  width: 900px;
}
</style>
