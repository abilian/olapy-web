<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              Select columns to use in <u>good order</u> <b>(including the id column)</b>
              <div v-for="(columns, columns_index) in selectTableColumns">
                <div v-for="(column, column_index) in columns" style="float: left">
                  <label :for="column">
                    <input v-model="selectedColumns['columns']" :key="columns_index + column_index" type="checkbox" :value="column">
                    {{column}}
                  </label>
                </div>
              </div>
            </slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">
              <div>
                Selected :
                <ol>
                  <li v-for="column in selectedColumns['columns']">
                    {{ column }}
                  </li>
                </ol>
              </div>

              <button class="modal-default-button" @click="saveChoseCol()">
                Save
              </button>


              <button class="modal-default-button" @click="closeChoseCol()">
                Close
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
    selectTableColumns: String,
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
