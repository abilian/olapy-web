<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              <table class="table" style="width: 100%">
                <tr>
                  <th>Dimensions :</th>
                  <th></th>
                  <th>{{ factsTable }}</th>
                </tr>
                <tr>
                  <!-- <td> -->
                  <!-- </td> -->
                </tr>
                <tr
                  v-for="(table, index) in tablesAndColumns"
                  :key="table + index"
                  v-if="index !== factsTable"
                >
                  <td>
                    <label> {{ index }} : </label>
                  </td>
                  <td>
                    <label>
                      <select
                        class="form-control"
                        v-model="tablesAndColumnsResult[index]['DimCol']"
                      >
                        <option
                          v-for="(item, index) in tablesAndColumns[index]"
                          :key="item + index"
                          :value="item"
                        >
                          {{ item }}
                        </option>
                      </select>
                    </label>
                    &rArr;
                  </td>
                  <td>
                    <label>
                      <select
                        class="form-control"
                        style="float: left"
                        v-model="tablesAndColumnsResult[index]['FactsCol']"
                      >
                        <option
                          v-for="(item, index) in tablesAndColumns[factsTable]"
                          :key="index"
                          :value="item"
                        >
                          {{ item }}
                        </option>
                      </select>
                    </label>
                  </td>
                </tr>
              </table>
            </slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">
              <button class="btn btn-btn" @click="$emit('close', false)">
                close
              </button>
              <button class="btn btn-primary" @click="confirmRelations()">
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
    factsTable: String,
    chosenTables: Array,
    chosenMeasures: Array,
    dbConfig: String,
  },

  data: function () {
    return {
      tablesAndColumns: "",
      result: "",
      tablesAndColumnsResult: {},
    };
  },

  created() {
    const allTables = [this.factsTable];
    for (let key in this.chosenTables) {
      allTables.push(this.chosenTables[key].name);
    }
    const data = {
      dbConfig: this.dbConfig,
      allTables: allTables.join(","),
    };
    axios.post("/api/cubes/get_tables_and_columns", data).then((result) => {
      this.tablesAndColumns = result.data;
      for (let key in result.data) {
        if (key !== this.factsTable) {
          this.tablesAndColumnsResult[key] = {
            DimCol: "",
            FactsCol: "",
          };
        }
      }
    });
  },

  methods: {
    confirmRelations: function () {
      this.$emit("tablesAndColumnsResult", this.tablesAndColumnsResult);
      eventModalBus.modalToShow("confirmCustomCube");
    },
  },
};
</script>

<style scoped>
.modal-container {
  width: 50%;
}
</style>
