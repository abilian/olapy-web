<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              {{cube}}
              {{cubeName}}
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

  // import {eventModalBus} from '../schema-options.vue'

  export default {
    props: ['cube', 'cubeName'],
    methods: {
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
