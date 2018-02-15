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
              <div v-for="column in tableColumns" style="float: left">
                <label :for="column">
                  {{column}} <input type="checkbox" :id="column" :value="column"
                                    v-model="measures">
                </label>
              </div>

              <div v-for="(table, index) in tables">
                <label>
                  <select v-model="table.name">
                    <option v-for="item in cube.dimensions" :value="item">{{ item }}
                    <option>
                  </select>
                </label>
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
        tableColumns: '',
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
        eventModalBus.modalToShow('makeRelations');
      }
    },
    watch: {
      factsTable: function () {
        this.$http.post('cubes/get_table_columns_no_id', this.factsTable)
          .then(x => {
            this.tableColumns = x.data;
          })
      }
    }
  }

</script>

<style scoped>
</style>
