<template>
  <div>

    <div v-if="reportingInterface !== 'dashboardMaker'">
      <input type="button" value="new dashboard" @click="reportingInterface = 'dashboardMaker'"/>
      <!--<select-cube-dashboard v-if="reportingInterface === 'newDashboard'"-->
      <!--@selectedCube="selectedCube = $event" @interface="reportingInterface = $event"/>-->
      <!--<hr>-->
      <user-dashboards @selectedDashboard="selectedDashboard = $event"
                       @reportingInterface="reportingInterface = $event"/>
    </div>

    <dashboard-marker v-if="reportingInterface === 'dashboardMaker'" :selectedDashboard="selectedDashboard" @interface="reportingInterface = $event"/>

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
