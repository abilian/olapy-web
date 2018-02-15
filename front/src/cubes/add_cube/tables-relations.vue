<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              <!--<div v-for="(table, index) in tablesAndColumns">-->
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
                    <select v-model="tablesAndColumnsResult[index]['DimCol']">
                      <option v-for="item in tablesAndColumns[index]" :value="item">{{ item }}
                      <option>
                    </select>
                    &rArr;
                  </td>
                  <td>
                    <label>
                      <select  style="float: left;" v-model="tablesAndColumnsResult[index]['FactsCol']">
                        <option v-for="item in tablesAndColumns[factsTable]" :value="item">{{ item }}
                        <option>
                      </select>
                    </label>
                  </td>
                </tr>
              </table>
              <!--<button type="button" v-on:click="removeSection(index)">Remove</button>-->
              <!--selected: {{table.name}}-->
              <!--</div>-->

            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="confirmRelations()">
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

  // import {eventModalBus} from '../schema-options.vue'

  export default {
    props: ['factsTable', 'chosenTables'],
    data: function () {
      return {
        tablesAndColumns: '',
        result: '',
        tablesAndColumnsResult: {}
      }
    },
    methods: {
      confirmRelations: function () {
        alert('hello');
        // eventModalBus.modalToShow('makeRelations');
      }
    },
    created() {

      let allTables = [this.factsTable];
      for (let key in this.chosenTables) {
        allTables.push(this.chosenTables[key].name);
      }

      this.$http.post('cubes/get_tables_and_columns', allTables.join(','))
        .then(x => {
          this.tablesAndColumns = x.data;
          for (let key in x.data) {
            if (key !== this.factsTable) {
              this.tablesAndColumnsResult[key] = {
                'DimCol': '',
                'FactsCol': ''
              };
            }
          }
          // this.tablesAndColumnsResult.keys()
        })
      //   else {
      //     this.$emit('uploadStatus', 'toConfig');
      //   }
      //   eventModalBus.cubeConstructed(x.data);
      //   this.currentStatus = STATUS_SUCCESS;
      // })


    }
  }

</script>

<style scoped>
</style>
