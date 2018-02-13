<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            <label>
              Cube Name :

              <input type="text" v-model="newCubeName">
            </label>

            <label style="margin-left: 70px">
              Source :
              <select v-model="source">
                <option disabled value="">Choisissez</option>
                <option>CSV</option>
                <option>DataBase</option>
              </select>
            </label>

          </div>

          <div class="modal-body">
            <slot name="body">
              <uploadCsvFiles :newCubeName="newCubeName" v-show="source == 'CSV'"
                              @uploadStatus="status = $event"></uploadCsvFiles>
              <connectDb v-show="source == 'DataBase'"></connectDb>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--<button class="modal-default-button" @click="$emit('uploadStatus', 'second')">-->
              <button class="modal-default-button" @click="checkUpload();  $emit('newCubeName', newCubeName)">
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

  import uploadFiles from './upload-files';
  import connectDb from './connect-db';
  import {eventModalBus} from '../schema-options.vue';

  export default {
    data: function () {
      return {
        newCubeName: '',
        source: '',
        status: 'failed',
      }
    },
    methods: {
      checkUpload() {
        if (this.status === 'failed') {
          eventModalBus.modalToShow('first');
        }
        else if (this.status === 'success') {
          if (this.newCubeName !== '') {
            // eventModalBus.newCubeName(this.newCubeName);
            eventModalBus.modalToShow('second');
          }
          else alert('Please specify a Cube name ')
        }
      }
    },
    components: {
      uploadCsvFiles: uploadFiles,
      connectDb: connectDb
    }

  }
</script>

<style>
  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
    display: table;
    transition: opacity .3s ease;
  }

  .modal-wrapper {
    display: table-cell;
    vertical-align: middle;
  }

  .modal-container {
    width: 70%;
    height: 50%;
    margin: 0px auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
  }

  .modal-header h3 {
    margin-top: 0;
    color: #42b983;
  }

  .modal-body {
    margin: 20px 0;
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
