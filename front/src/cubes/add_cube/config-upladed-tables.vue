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
              <div v-for="(measure, index) in this.cube.measures">

                <label>
                  <input type="text" :key="index" :value="measure">
                </label>
              </div>

              <hr>
              Dimensions :
              <div v-for="(dimension, index) in this.cube.dimensions">

                <label>
                  <input type="text" :key="index" :value="dimension">
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
              <button class="modal-default-button" @click="$emit('close', false)">
                close
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>

</template>

<script>
import { eventModalBus } from "../base-schema-options";

export default {
  props: {
    cube: Object,
    cubeName: String,
    dbConfig: String,
  },
  methods: {
    confirmCube: function() {
      if (this.dbConfig !== "") {
        this.$http
          .post("api/cubes/confirm_db_cube", this.dbConfig)
          .then(response => {
            eventModalBus.modalToShow("success");
            return response.json();
          });
      } else {
        let data = {
          cubeName: this.cubeName,
          customCube: false,
        };
        this.$http.post("api/cubes/confirm_cube", data).then(response => {
          eventModalBus.modalToShow("success");
          return response.json();
        });
      }
    },
  },
};
</script>

<style scoped>
</style>
