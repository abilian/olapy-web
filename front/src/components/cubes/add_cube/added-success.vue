<template>
  <!-- <transition name="modal"> -->
  <!-- <div class="modal-mask"> -->
  <!-- <div class="modal-wrapper"> -->
  <!-- <div class="modal-container"> -->

  <!-- <div class="modal-body"> -->
  <!-- <slot name="body"> -->
  <!-- Cube Added successfully -->
  <!-- </slot> -->
  <!-- </div> -->

  <!-- <div class="modal-footer"> -->
  <!-- <slot name="footer"> -->
  <!--
    &lt;!&ndash;<button class="modal-default-button" @click="$emit('uploadStatus', 'second')">&ndash;&gt;
  -->
  <!--
    &lt;!&ndash;<button class="modal-default-button" @click="checkUpload()">&ndash;&gt;
  -->
  <!-- <button class="modal-default-button" @click="goBack()"> -->
  <!-- Next -->
  <!-- </button> -->
  <!-- </slot> -->
  <!-- </div> -->
  <!-- </div> -->
  <!-- </div> -->
  <!-- </div> -->
  <!-- </transition> -->
</template>

<script>
import { eventModalBus } from "../base-add-cube.vue";

export default {
  created() {
    this.$notify({
      group: "user",
      title: this.cubeName + "Successfully Added",
      type: "success",
    });
    this.$emit("close", false);
    eventModalBus.modalToShow("first");
  },
};
</script>

<style scoped></style>
