<template>
    <li id="cubes-names">

        <div class="nav-btn">
            <button class="white-btn" @click="$emit('reportingInterface', 'addCube')">
                <i class="fa fa-table"></i>
                <span>Cubes</span>
            </button>
        </div>

        <a class="has-arrow  " href="#" aria-expanded="false">
            <span class="hide-menu">
            <span class="label label-rouded label-danger pull-right">{{cubesNames.length}}</span>
        </span>
        </a>
        <ul aria-expanded="false" class="collapse">
            <li v-for="cube in cubesNames">
                <button class="btn btn-default btn-outline btn-rounded m-b-10">{{cube}}</button>
            </li>


        </ul>
    </li>

</template>

<script>
export default {
  props: {
    refreshCubes: Boolean,
  },
  data: function() {
    return {
      cubesNames: [],
    };
  },
  methods: {
    getCubes: function() {
      let cubes = [];
      this.$http
        .get("api/cubes")
        .then(response => {
          return response.json();
        })
        .then(data => {
          for (let key in data) {
            cubes.push(data[key]);
          }
        });
      this.cubesNames = cubes;
    },
  },
  watch: {
    refreshCubes: function(val) {
      if (val === true) {
        this.getCubes();
        this.$emit("refreshCubes", false);
      }
    },
  },
  created() {
    this.getCubes();
  },
};
</script>

<style scoped>
.schema_box {
  position: relative;
  float: left;
  top: 30px;
  left: 10px;
  width: 195px;
  height: 480px;
  border: 1px solid #98a6ad;
}

.schema_box_container {
  margin-left: 4px;
  margin-top: 10px;
}
</style>
