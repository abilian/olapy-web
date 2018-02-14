<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              <label>
                <input type="text" :value="cubeName">
              </label>

              <div v-for="(table, index) in tables">
                <label>
                  <select v-model="table.name">
                    <option v-for="item in cube.dimensions" :value="item">{{ item }}
                    <option>
                  </select>
                </label>
                <button type="button" v-on:click="removeSection(index)">Remove Me</button>
                selected: {{table.name}}
              </div>
              <button type="button" v-on:click="addComponent()">Select New Table</button>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="confirmCube()">
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

    props: ['cube', 'cubeName'],
    data: function () {
      return {
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

      confirmCube: function () {
        alter('hello')
        // this.$http.post('cubes/confirm_cube', this.cubeName)
        //   .then(response => {
        //     eventModalBus.modalToShow('success');
        //     return response.json();
        //   });

      },
    }
  }

</script>

<style scoped>
</style>
