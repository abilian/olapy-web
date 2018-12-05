<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="body">
              Facts table :
              <span class="badge badge-light">{{ cube.facts }}</span>

              <br />
              Measures :
              <span
                v-for="measure in cube.measures"
                class="badge badge-light"
                >{{ measure }}</span
              >
              <br />
              Dimensions :
              <span
                v-for="dimension in this.cube.dimensions"
                class="badge badge-light"
                >{{ dimension }}</span
              >
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--
                <button class="modal-default-button" @click="$emit('uploadStatus', 'second')">
              -->
              <!--
                <button class="modal-default-button" @click="checkUpload()">
              -->
              <button class="btn btn-btn" @click="$emit('close', false);">
                close
              </button>
              <button class="btn btn-primary" @click="confirmCube();">
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
const axios = require("axios");
import { eventModalBus } from "../base-add-cube";

export default {
  props: {
    cube: Object,
    cubeName: String,
    dbConfig: String,
  },
  methods: {
    confirmCube: function() {
      if (this.dbConfig !== "") {
        axios
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
        axios.post("api/cubes/confirm_cube", data).then(response => {
          eventModalBus.modalToShow("success");
          return response.json();
        });
      }
    },
  },
};
</script>

<style scoped></style>
