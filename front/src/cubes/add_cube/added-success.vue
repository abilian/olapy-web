<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              Cube Added successfully
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--<button class="modal-default-button" @click="$emit('uploadStatus', 'second')">-->
              <!--<button class="modal-default-button" @click="checkUpload()">-->
              <button class="modal-default-button" @click="goBack()">
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
import { eventModalBus } from "../schema-options.vue";

export default {
  methods: {
    goBack() {
      this.$emit("close", false);
      eventModalBus.modalToShow("first");
    },
  },
};
</script>

<style scoped>
</style>
