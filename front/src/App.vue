<template>
  <div>
    <div class="left-sidebar">
      <!-- Sidebar scroll -->
      <div class="scroll-sidebar">
        <!-- Sidebar navigation -->
        <nav class="sidebar-nav">
          <ul id="sidebarnav">
            <li class="nav-devider"></li>
            <li class="nav-label">Home</li>
            <!--
              refreshDashboards used to refresh user-dashboards: every time i add dashboard from \
              dash-maker component, i want to refresh user-dashboards component (maybe another solution is better
            -->
            <user-dashboards
              @selectedDashboard="selectedDashboard = $event;"
              @reportingInterface="reportingInterface = $event;"
              @refreshDashboards="refreshDashboards = $event;"
              :refreshDashboards="refreshDashboards"
            />

            <user-cubes
              @reportingInterface="reportingInterface = $event;"
              @refreshCubes="refreshCubes = $event;"
              :refreshCubes="refreshCubes"
            >
            </user-cubes>

            <user-pivot-tables
              @selectedPivotTable="selectedPivotTable = $event;"
              @reportingInterface="reportingInterface = $event;"
              @refreshPivotTables="refreshPivotTables = $event;"
              :refreshPivotTables="refreshPivotTables"
            />
            <!-- <li> -->
            <!--
              <a href="#" aria-expanded="false"><i class="fa fa-columns"></i>
            -->
            <!--
              <span @click="reportingInterface='QBuilder'" class="hide-menu">Query Builder</span>
            -->
            <!-- </a> -->
            <!-- <ul aria-expanded="false" class="collapse"> -->
            <!-- </ul> -->
            <!-- </li> -->
          </ul>
        </nav>
        <!-- End Sidebar navigation -->
      </div>
      <!-- End Sidebar scroll -->
    </div>

    <div class="page-wrapper" v-if="reportingInterface === 'main'">
      <div class="row page-titles">
        <div class="col-md-5 align-self-center">
          <button
            type="button"
            class="btn btn-primary btn-flat btn-addon m-b-10 m-l-5"
            @click="reportingInterface = 'dashboardMaker';"
          >
            <i class="ti-plus"></i>New Dashboard
          </button>
        </div>
      </div>
    </div>

    <dashboard-maker
      v-if="reportingInterface === 'dashboardMaker'"
      @refreshDashboards="refreshDashboards = $event;"
      @reportingInterface="reportingInterface = $event;"
      :selectedDashboard="selectedDashboard"
    />

    <schema-options
      v-if="reportingInterface === 'addCube'"
      @refreshCubes="refreshCubes = $event;"
    >
    </schema-options>
    <!-- <keep-alive> -->
    <query-builder
      @refreshPivotTables="refreshPivotTables = $event;"
      :selectedPivotTable="selectedPivotTable"
      v-if="reportingInterface === 'QBuilder'"
    ></query-builder>
    <!-- </keep-alive> -->

    <notifications group="user" position="top center" />
  </div>
</template>

<script>
import Cubes from "./cubes/the-cubes-names.vue";
import UserDashboards from "./reporting/userDashboards";
import DashboardMaker from "./reporting/dashboardMaker";
import QueryBuilder from "./reporting/queryBuilder";
import SchemaOptions from "./cubes/base-add-cube";
import UserPivotTables from "./reporting/userPivotTables";

export default {
  data: function() {
    return {
      reportingInterface: "main",
      selectedDashboard: null,
      selectedPivotTable: null,
      refreshDashboards: false,
      refreshPivotTables: false,
      refreshCubes: false,
    };
  },
  components: {
    UserPivotTables,
    userCubes: Cubes,
    schemaOptions: SchemaOptions,
    userDashboards: UserDashboards,
    dashboardMaker: DashboardMaker,
    queryBuilder: QueryBuilder,
  },
};
</script>

<style>
/*used in user-dashboards, user-cubes and user-pivot-tables  */
.has-arrow {
  margin-left: 79%;
  width: 15%;
  height: 33px;
}

/*used in user-dashboards, user-cubes and user-pivot-tables  */
.nav-btn {
  width: 65%;
  float: left;
  margin-left: 5%;
  margin-top: 2%;
}

/*used in user-dashboards, user-cubes and user-pivot-tables  */
.white-btn {
  background-color: #fff0;
  background-repeat: no-repeat;
  border: none;
  cursor: pointer;
  overflow: hidden;
  outline: none;
  color: #47657b;
}

.white-btn span {
  margin-left: 5px;
}
</style>
