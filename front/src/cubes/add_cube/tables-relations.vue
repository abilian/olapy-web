<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              <table class="table" style="width: 100%">
                <tr>
                  <th> Dimensions :</th>
                  <th></th>
                  <th>{{factsTable}}</th>
                </tr>
                <tr>
                  <td>
                  </td>
                </tr>
                <tr v-for="(table, index) in tablesAndColumns" v-if="index !== factsTable">
                  <td>
                    <label>
                      {{index}} :
                    </label>
                  </td>
                  <td>
                    <label>
                      <select v-model="tablesAndColumnsResult[index]['DimCol']">
                        <option v-for="item in tablesAndColumns[index]" :value="item">{{ item }}
                        <option>
                      </select>
                    </label>
                    &rArr;
                  </td>
                  <td>
                    <label>
                      <select style="float: left;" v-model="tablesAndColumnsResult[index]['FactsCol']">
                        <option v-for="item in tablesAndColumns[factsTable]" :value="item">{{ item }}
                        <option>
                      </select>
                    </label>
                  </td>
                </tr>
              </table>
            </slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="confirmRelations()">
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
import { eventModalBus } from "../schema-options.vue";

export default {
  props: ["factsTable", "chosenTables", "chosenMeasures", "dbConfig"],
  data: function() {
    return {
      tablesAndColumns: "",
      result: "",
      tablesAndColumnsResult: {},
    };
  },
  methods: {
    confirmRelations: function() {
      this.$emit("tablesAndColumnsResult", this.tablesAndColumnsResult);
      eventModalBus.modalToShow("confirmCustomCube");
    },
  },
  created() {
    let allTables = [this.factsTable];
    for (let key in this.chosenTables) {
      allTables.push(this.chosenTables[key].name);
    }
    let data = {
      dbConfig: this.dbConfig,
      allTables: allTables.join(","),
    };
    this.$http.post("api/cubes/get_tables_and_columns", data).then(x => {
      this.tablesAndColumns = x.data;
      for (let key in x.data) {
        if (key !== this.factsTable) {
          this.tablesAndColumnsResult[key] = {
            DimCol: "",
            FactsCol: "",
          };
        }
      }
    });
  },
};
</script>

<style scoped>
</style>
