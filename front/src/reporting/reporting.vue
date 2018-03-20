<template>
  <div>

    <div  v-if="reportingInterface !== 'dashboardMaker'">
      <input type="button" value="new dashboard" @click="reportingInterface = 'newDashboard'"/>
      <select-cube-dashboard v-if="reportingInterface === 'newDashboard'" @dashboardName="dashboardName = $event"
                             @selectedCube="selectedCube = $event" @interface="reportingInterface = $event"/>
      <hr>
      <user-dashboards/>
    </div>

    <dashboard-marker v-if="reportingInterface === 'dashboardMaker'" :dashboardName="dashboardName"
                      :selectedCube="selectedCube" @interface="reportingInterface = $event"/>

  </div>
</template>


<script>
import selectCubeDashboard from "./selectCubeDashboard";
import userDashboards from "./userDashboards";
import dashboardMarker from "./dashboardMaker";

export default {
  data: function() {
    return {
      reportingInterface: "main",
    };
  },
  components: {
    "select-cube-dashboard": selectCubeDashboard,
    "user-dashboards": userDashboards,
    "dashboard-marker": dashboardMarker,
  },
};
</script>

<style>
</style>
