<template>
  <div>
    <input type="button" value="new dashboard" @click="selectCubeModal = true"/>

    <select-cube-dashboard v-show="selectCubeModal"/>
    <hr>
    <user-dashboards/>
  </div>
</template>


<script>
import selectCubeDashboard from "./selectCubeDashboard";
import userDashboards from "./userDashboards";

export default {
  data: function() {
    return {
      selectCubeModal: false,
    };
  },
  components: {
    "select-cube-dashboard": selectCubeDashboard,
    "user-dashboards": userDashboards,
  },
};
</script>

<style>

</style>
