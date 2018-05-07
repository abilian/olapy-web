<template>
  <div>
    <div class="left-sidebar">
      <!-- Sidebar scroll-->
      <div class="scroll-sidebar">
        <!-- Sidebar navigation-->
        <nav class="sidebar-nav">
          <ul id="sidebarnav">
            <li class="nav-devider"></li>
            <li class="nav-label">Home</li>
            <user-dashboards @selectedDashboard="selectedDashboard = $event"
                             @reportingInterface="reportingInterface = $event"/>
            <user-cubes @reportingInterface="reportingInterface = $event"></user-cubes>
          </ul>
        </nav>
        <!-- End Sidebar navigation -->
      </div>
      <!-- End Sidebar scroll-->

    </div>

      <div class="page-wrapper" v-if="showNewDashBtn && reportingInterface==='main'">
          <div class="row page-titles">
              <div class="col-md-5 align-self-center">
                  <button type="button" class="btn btn-primary btn-flat btn-addon m-b-10 m-l-5"
                          @click="showNewDashBtn=false"><i class="ti-plus"></i>New Dashboard
                  </button>
              </div>
          </div>
      </div>

      <dashboard-maker v-if="!showNewDashBtn || reportingInterface==='dashboardMaker' "
                       :selectedDashboard="selectedDashboard"
                       @hideNewDashBtn="showNewDashBtn = $event"/>


      <schema-options v-if="reportingInterface==='addCube' "></schema-options>

  </div>


</template>


<script>
import Cubes from "./cubes/the-cubes-names.vue";
import UserDashboards from "./reporting/userDashboards";
import DashboardMaker from "./reporting/dashboardMaker";
import SchemaOptions from "./cubes/base-schema-options";

export default {
  data: function() {
    return {
      reportingInterface: "main",
      showNewDashBtn: true,
      selectedDashboard: "",
    };
  },
  components: {
    userCubes: Cubes,
    schemaOptions: SchemaOptions,
    userDashboards: UserDashboards,
    dashboardMaker: DashboardMaker,
  },
};
</script>

<style>
</style>
