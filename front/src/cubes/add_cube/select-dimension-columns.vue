<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            Select columns to use in <u>good order</u> <b>(including the id column)</b>
          </div>

          <div class="modal-body">
            <slot name="body" v-for="columns in selectTableColumns">
              <label v-for="column in columns">
                {{column}}
                <input v-model="selectedColumns['columns']" type="checkbox"
                       :value="column">
              </label>

            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="btn btn-btn" @click="closeChoseCol()">
                Close
              </button>
              <button class="btn btn-primary" @click="saveChoseCol()">
                Save
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
    selectTableColumns: Object,
  },
  data: function() {
    return {
      selectedColumns: {
        table: Object.keys(this.selectTableColumns)[0],
        columns: [],
      },
    };
  },
  methods: {
    saveChoseCol() {
      {
        this.$emit("SavedColumns", this.selectedColumns);
        eventModalBus.modalToShow("toConfig");
      }
    },
    closeChoseCol() {
      {
        eventModalBus.modalToShow("toConfig");
      }
    },
  },
};
</script>

<style scoped>
</style>
