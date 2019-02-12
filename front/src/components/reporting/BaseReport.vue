<template>
  <div>
    <div class="row page-titles" v-if="reportingInterface === 'main'">
      <div class="col-md-5 align-self-center">
        <!-- <h3 class="text-primary">Dashboard</h3> -->
        <button
          type="button"
          class="btn btn-primary btn-flat btn-addon m-b-10 m-l-5"
          @click="reportingInterface = 'dashboardMaker'"
        >
          <i class="ti-plus"></i>New Dashboard
        </button>
      </div>
    </div>

    <!-- End Bread crumb -->
    <!-- Container fluid -->

    <div class="container-fluid">
      <dashboard-marker
        v-if="reportingInterface === 'dashboardMaker'"
        :selectedDashboard="selectedDashboard"
        @interface="reportingInterface = $event"
      />
    </div>
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

<style></style>
