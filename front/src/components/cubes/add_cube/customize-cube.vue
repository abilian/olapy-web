<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              <!-- <label v-if="dbConfig === ''"> -->
              <!-- Cube Name: -->
              <!--
                <input placeholder="Cube name" type="text" :value="cubeName">
              -->
              <!-- </label> -->
              <input
                class="form-control"
                v-if="dbConfig === ''"
                placeholder="Cube name"
                type="text"
                :value="cubeName"
              />
              <br />
              <select class="form-control" v-model="factsTable">
                <option disabled value="">Facts Table</option>
                <option
                  v-for="(item, index) in cube.dimensions"
                  :key="index"
                  :value="item"
                  >{{ item }}
                </option>
              </select>
              <br />
              <div>
                <span>Measures :</span><br />
                <!-- <span>Measures : {{ measures.join(', ') }}</span><br> -->
                <!--
                  <div v-for="(column, index) in tableColumnsNoId" style="float: left">
                -->
                <label
                  v-for="(column, index) in tableColumnsNoId"
                  :key="column + index"
                  style="float: left"
                  :for="column"
                >
                  {{ column }}
                  <input
                    type="checkbox"
                    :id="column"
                    :key="index"
                    :value="column"
                    v-model="measures"
                  />
                </label>
                <!-- </div> -->
              </div>

              <select
                title="Dimensions"
                v-for="(table, index) in tables"
                class="form-control"
                v-model="table.name"
                :key="index"
                @change="updateTableColumns(table.name, index)"
              >
                <option disabled value="">Dimensions</option>
                <option
                  v-for="(item, index) in cube.dimensions"
                  :key="index"
                  :value="item"
                  >{{ item }}
                </option>
              </select>
              <i
                class="fa fa-times"
                aria-hidden="true"
                @click="removeSection(index)"
              ></i>
              <i class="far fa-edit" @click="editColumns()"></i>
              <!--
                <button type="button" @click="editColumns()">Select Columns</button>
              -->

              <i class="fas fa-plus" @click="addComponent()"></i>
              <!--
                <button type="button" @click="addComponent()">Select New Table</button>
              -->
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="btn btn-default" @click="$emit('close', false)">
                close
              </button>
              <button class="btn btn-primary" @click="doRelations()">
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
    cube: Object,
    cubeName: String,
    SavedColumns: Object,
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
      const data = {
        tableName: tableName,
        WithID: true,
        dbConfig: this.dbConfig,
      };
      axios.post("/api/cubes/get_table_columns", data).then(response => {
        const table_columns = {};
        table_columns[tableName] = response.data;
        this.tableColumns[index] = table_columns;
        this.$emit("selectTableColumns", this.tableColumns[index]);
        eventModalBus.modalToShow("choseColumns");
      });
    },
  },
  watch: {
    factsTable: function() {
      const data = {
        tableName: this.factsTable,
        WithID: false,
        dbConfig: this.dbConfig,
      };
      axios.post("/api/cubes/get_table_columns", data).then(response => {
        this.tableColumnsNoId = response.data;
      });
    },
  },
};
</script>
