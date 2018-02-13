<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">

              <label>
                Facts table :
                <input type="text" :value="this.cube.facts">
              </label>

              <hr>
              Measures :
              <div v-for="measure in this.cube.measures">

                <label>
                  <input type="text" :value="measure">
                </label>
              </div>

              <hr>
              Dimensions :
              <div v-for="dimension in this.cube.dimensions">

                <label>
                  <input type="text" :value="dimension">
                </label>
              </div>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--<button class="modal-default-button" @click="$emit('uploadStatus', 'second')">-->
              <!--<button class="modal-default-button" @click="checkUpload()">-->
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

  import {eventModalBus} from '../schema-options.vue'

  export default {
    props: ['cube'],
    methods: {
      confirmCube: function () {
        this.$http.get('cubes/confirm_cube')
          .then(response => {
            eventModalBus.modalToShow('success');
            return response.json();
          });

      },
    }
  }

</script>

<style scoped>
</style>
