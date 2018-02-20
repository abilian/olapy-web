<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              <label>
                Cube Name:
                <input type="text" :value="cubeName">
              </label>
              <label>
                Facts :
                <select v-model="factsTable">
                  <option v-for="item in cube.dimensions" :value="item">{{ item }}
                  <option>
                </select>
              </label>
              selected: {{factsTable}}
              <hr>
              <span>Measures : {{ measures.join(', ') }}</span><br>
              <div v-for="column in tableColumnsNoId" style="float: left">
                <label :for="column">
                  {{column}} <input type="checkbox" :id="column" :value="column"
                                    v-model="measures">
                </label>
              </div>

              <div v-for="(table, index) in tables">
                <label>
                  <select v-model="table.name" @change="updateTableColumns(table.name, index)">
                    <option v-for="item in cube.dimensions" :value="item">{{ item }}
                    <option>
                  </select>
                </label>

                <div v-for="columns in tableColumns[index]">
                  <div v-for="column in columns" style="float: left">
                    <label :for="column">
                      {{column}} <input type="checkbox" :id="column" :value="column">
                      <!--v-model="measures">-->
                    </label>
                  </div>
                </div>

                <button type="button" v-on:click="removeSection(index)">Remove</button>
                <!--selected: {{table.name}}-->
              </div>
              <button type="button" v-on:click="addComponent()">Select New Table</button>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="doRelations()">
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

  import {eventModalBus} from '../schema-options.vue'

  export default {

    props: ['cube', 'cubeName'],
    data: function () {
      return {
        factsTable: '',
        measures: [],
        tableColumnsNoId: '',
        tableColumns: {},
        tables: [{
          id: "1",
          name: ''
        }]
      }
    },
    methods: {
      removeSection: function (index) {
        this.tables.splice(index, 1)
      },
      addComponent: function () {
        this.tables.push({
          id: Math.floor(Math.random() * 6),
          name: ''
        });
      },
      doRelations: function () {
        this.$emit('factsTable', this.factsTable);
        this.$emit('chosenTables', this.tables);
        this.$emit('chosenMeasures', this.measures);
        eventModalBus.modalToShow('makeRelations');
      },
      updateTableColumns(tableName, index) {
        this.$http.post('cubes/get_table_columns', {
          'tableName': tableName,
          'WithID': true
        }).then(x => {
          let table_columns = {};
          table_columns[tableName] = x.data;
          this.tableColumns[index] = table_columns;
          this.$emit('selectTable', this.tableColumns[index]);
          eventModalBus.modalToShow('choseColumns');
        });

      },
    }
    ,
    watch: {
      factsTable: function () {
        this.$http.post('cubes/get_table_columns', {
          'tableName': this.factsTable,
          'WithID': false
        }).then(x => {
          this.tableColumnsNoId = x.data;
        })
      }
    }

  }

</script>

<style scoped>
</style>
