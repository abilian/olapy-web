<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
          </div>

          <div class="modal-body">
            <slot name="body">
              <label>
                <select v-model="selectedCube">
                  <option disabled value="">Choose</option>
                    <option v-for="cube in userCubes">
                      {{ cube }}
                    </option>
                </select>
              </label>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--<button class="modal-default-button" @click="$emit('SelectInputStatus', 'second')">-->
              <button class="modal-default-button" @click="validateCubeSelection()">
                Next
              </button>
              <button class="modal-default-button" @click="$emit('interface', 'main')">
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
export default {
  data: function() {
    return {
      selectedCube: "",
      userCubes: [],
    };
  },
  methods: {
    validateCubeSelection() {
      if (this.selectedCube) {
        this.$emit("selectedCube", this.selectedCube);
        this.$emit("interface", "dashboardMaker");
      }
    },
  },
  created() {
    this.$http
      .get("api/cubes")
      .then(response => {
        return response.json();
      })
      .then(data => {
        for (let key in data) {
          this.userCubes.push(data[key]);
        }
      });
  },
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
  width: 70%;
  height: 50%;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
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

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
