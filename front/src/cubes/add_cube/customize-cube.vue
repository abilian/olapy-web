<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              <label v-if="dbConfig === ''">
                Cube Name:
                <input type="text" :value="cubeName">
              </label>
              <label>
                Facts :
                <select v-model="factsTable">
                  <option v-for="(item, index) in cube.dimensions" :key="index" :value="item">{{ item }}
                  <option>
                </select>
              </label>
              <span>Measures : {{ measures.join(', ') }}</span><br>
              <div v-for="(column, index) in tableColumnsNoId" style="float: left">
                <label :for="column">
                  {{column}} <input type="checkbox" :id="column" :key="index" :value="column"
                                    v-model="measures">
                </label>
              </div>
              <br>
              <hr>
              <div v-for="(table, index) in tables">
                <label>
                  <select v-model="table.name" :key="index" @change="updateTableColumns(table.name, index)">
                    <option v-for="(item, index) in cube.dimensions" :key="index" :value="item">{{ item }}
                    <option>
                  </select>
                </label>
                <button type="button" @click="removeSection(index)">Remove</button>
                <button type="button" @click="editColumns()">Select Columns</button>
              </div>
              <button type="button" @click="addComponent()">Select New Table</button>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="doRelations()">
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
    cube: String,
    cubeName: String,
    SavedColumns: String,
    dbConfig: String,
  },
  data: function() {
    return {
      DimColumns: [],
      factsTable: "",
      measures: [],
      tableColumnsNoId: "",
      tableColumns: {},
      tables: [
        {
          id: "1",
          name: "",
        },
      ],
    };
  },
  methods: {
    removeSection: function(index) {
      this.tables.splice(index, 1);
    },
    addComponent: function() {
      this.tables.push({
        id: Math.floor(Math.random() * 6),
        name: "",
      });
      this.DimColumns.push(this.SavedColumns);
    },
    editColumns() {
      eventModalBus.modalToShow("choseColumns");
    },
    doRelations: function() {
      this.$emit("factsTable", this.factsTable);
      this.$emit("chosenTables", this.tables);
      this.$emit("chosenMeasures", this.measures);
      this.$emit("SavedColumns", this.DimColumns);
      eventModalBus.modalToShow("makeRelations");
    },
    updateTableColumns(tableName, index) {
      let data = {
        tableName: tableName,
        WithID: true,
        dbConfig: this.dbConfig,
      };
      this.$http.post("api/cubes/get_table_columns", data).then(x => {
        let table_columns = {};
        table_columns[tableName] = x.data;
        this.tableColumns[index] = table_columns;
        this.$emit("selectTableColumns", this.tableColumns[index]);
        eventModalBus.modalToShow("choseColumns");
      });
    },
  },
  watch: {
    factsTable: function() {
      let data = {
        tableName: this.factsTable,
        WithID: false,
        dbConfig: this.dbConfig,
      };
      this.$http.post("api/cubes/get_table_columns", data).then(x => {
        this.tableColumnsNoId = x.data;
      });
    },
  },
};
</script>

<style scoped>
</style>
