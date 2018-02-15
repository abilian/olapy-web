<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              {{cubeName}}
              <br>
              {{factsTable}}
              <br>
              {{tablesAndColumnsResult}}
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
    props: ['cubeName', 'factsTable', 'tablesAndColumnsResult'],
    data: function () {
      return {}
    },
    created() {
      let data = {
        cubeName : this.cubeName,
        factsTable: this.factsTable,
        tablesAndColumnsResult : this.tablesAndColumnsResult
      };
      console.log('ceaaateddd');
      this.$http.post('cubes/try_construct_custom_cube', data)
    }
  }

</script>

<style scoped>
</style>
