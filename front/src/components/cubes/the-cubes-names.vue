<template>
  <li id="cubes-names">
    <div class="nav-btn">
      <button class="white-btn" @click="$emit('reportingInterface', 'addCube')">
        <i class="fa fa-table"></i> <span>Cubes</span>
      </button>
    </div>

    <a class="has-arrow" href="#" aria-expanded="false">
      <span class="hide-menu">
        <span class="label label-rouded label-danger pull-right">{{
          userCubesNames.length
        }}</span>
      </span>
    </a>

    <ul aria-expanded="false" class="collapse">
      <li v-for="(cube, index) in userCubesNames" :key="cube + index">
        <button class="btn btn-default btn-outline btn-rounded m-b-10">
          {{ cube }}
        </button>

        <button
          class="delete-cube fa fa-times-circle-o fa-lg"
          @click="deleteCube(cube)"
        ></button>
      </li>
    </ul>
  </li>
</template>

<script>
import axios from "axios";

export default {
  props: {
    userCubesNames: Array,
  },

  methods: {
    deleteCube(cubeName) {
      const vue = this;
      this.$dlg.alert(
        "Are you sure to delete " + cubeName + " ?",
        function () {
          const data = { cubeName };
          axios.post("/api/cubes/delete", data);

          vue.$notify({
            group: "user",
            title: "Successfully Deleted",
            type: "success",
          });
          vue.$emit("removeUserCube", cubeName);
        },
        {
          messageType: "confirm",
          language: "en",
        }
      );
    },
  },
};
</script>

<style scoped>
.delete-cube {
  background-color: Transparent;
  background-repeat: no-repeat;
  border: none;
  cursor: pointer;
  float: right;
  margin: 6%;
}
</style>
