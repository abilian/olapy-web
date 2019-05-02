<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <select class="form-control" v-model="source">
              <option disabled value="">DataSource</option>
              <option>CSV</option>
              <option>DataBase</option>
            </select>
          </div>

          <div class="modal-body">
            <slot name="body">
              <div v-if="source === 'CSV'">
                <input
                  class="form-control"
                  placeholder="Cube Name"
                  type="text"
                  v-model="newCubeName"
                />
              </div>

              <upload-csv-files
                :newCubeName="newCubeName"
                v-show="source === 'CSV'"
                @SelectInputStatus="status = $event"
              />

              <connect-db
                v-show="source === 'DataBase'"
                @SelectInputStatus="status = $event"
              />
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--
                <button class="modal-default-button" @click="$emit('SelectInputStatus', 'second')">
              -->
              <button class="btn btn-default" @click="$emit('close', false)">
                close
              </button>
              <button
                class="btn btn-primary"
                @click="
                  checkUpload();
                  $emit('newCubeName', newCubeName);
                "
              >
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
import uploadFiles from "./upload-files";
import connectDb from "./connect-db";
import { eventModalBus } from "../base-add-cube.vue";

export default {
  data: function() {
    return {
      newCubeName: "",
      source: "",
      status: "failed"
    };
  },
  methods: {
    checkUpload() {
      if (this.status === "failed") {
        eventModalBus.modalToShow("first");
      } else if (this.source === "CSV" && this.newCubeName === "") {
        // this.$notify({
        //   group: "user",
        //   title: "Missing Cube name",
        //   type: "error",
        // });
        alert("Missing Cube name");
      } else if (this.status === "toConfig") {
        eventModalBus.modalToShow("toConfig");
      } else if (this.status === "success") {
        eventModalBus.modalToShow("second");
      }
    }
  },
  components: {
    uploadCsvFiles: uploadFiles,
    connectDb: connectDb
  }
};
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
  overflow: auto;
}

.modal-container {
  width: 40%;
  height: 50%;
  margin: 0 auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
  overflow: auto;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
  overflow: auto;
}

.modal-default-button {
  float: right;
}

/*
   * The following styles are auto-applied to elements with
   * transition="modal" when their visibility is toggled
   * by Vue.js.
   *
   * You can easily play with the modal transition by editing
   * these styles.
   */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
