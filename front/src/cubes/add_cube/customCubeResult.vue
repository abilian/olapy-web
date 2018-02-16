<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              <div class="table-responsive" v-html="resultCube">
              </div>
            </slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">
              <button
                class="modal-default-button"
                @click="confirmRelations()">
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
    props: ['cubeName', 'factsTable', 'tablesAndColumnsResult'],
    data: function () {
      return {
        resultCube: ''
      }
    },
    created() {
      let data = {
        cubeName: this.cubeName,
        factsTable: this.factsTable,
        tablesAndColumnsResult: this.tablesAndColumnsResult
      };
      console.log('ceaaateddd');
      this.$http.post('cubes/try_construct_custom_cube', data)
        .then(x => {
          this.resultCube = x.data;
        })
    }
  }

</script>

<style scoped>
  .modal-container {
    width: 900px;
  }
</style>
