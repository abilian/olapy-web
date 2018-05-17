<template>
    <li>
      <a class="has-arrow  " href="#" aria-expanded="false">
        <i class="fa fa-table"></i>
        <span @click="$emit('reportingInterface', 'addCube')" class="hide-menu">Cubes
            <span class="label label-rouded label-danger pull-right">{{cubesNames.length}}</span>
        </span>
      </a>
      <ul aria-expanded="false" class="collapse"  v-for="(cube, index) in cubesNames">
        <li><button class="btn btn-default btn-outline btn-rounded m-b-10" :key="index">{{cube}}</button></li>


      </ul>
    </li>

</template>

<script>
export default {
  data: function() {
    return {
      cubesNames: [],
    };
  },
  methods: {
    getCubes: function() {
      this.$http
        .get("api/cubes")
        .then(response => {
          return response.json();
        })
        .then(data => {
          for (let key in data) {
            this.cubesNames.push(data[key]);
          }
        });
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
