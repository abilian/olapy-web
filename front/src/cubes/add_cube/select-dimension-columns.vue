<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-body">
            <slot name="body">
              <!--zzzzzzzz {{selectTable}}-->
              <div v-for="columns in selectTable">
                <div v-for="column in columns" style="float: left">
                  <label :for="column">
                    {{column}} <input type="checkbox" :id="column" :value="column">
                    <!--v-model="measures">-->
                  </label>
                </div>
              </div>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="closeChoseCol()">
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

  import {eventModalBus} from '../schema-options.vue'

  export default {

    props: ['selectTable'],
    data: function () {
      return {}
    },
    methods: {
      closeChoseCol() {
        {
          eventModalBus.modalToShow('toConfig');
        }
      }

    }
  }

</script>

<style scoped>
</style>
