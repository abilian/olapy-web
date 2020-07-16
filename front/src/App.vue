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

            <user-cubes
              @removeUserCube="
                userCubesNames.splice(userCubesNames.indexOf($event), 1)
              "
              :userCubesNames="userCubesNames"
              @reportingInterface="reportingInterface = $event"
            >
            </user-cubes>

            <user-dashboards
              :userDashboards="userDashboards"
              @selectedDashboard="selectedDashboard = $event"
              @reportingInterface="reportingInterface = $event"
            />

            <user-pivot-tables
              :userPivotTables="userPivotTables"
              @selectedPivotTable="selectedPivotTable = $event"
              @reportingInterface="reportingInterface = $event"
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
            @click="reportingInterface = 'dashboardMaker'"
          >
            <i class="ti-plus"></i>New Dashboard
          </button>
        </div>
      </div>
    </div>

    <dashboard-maker
      @removeDashboard="
        userDashboards.splice(userDashboards.indexOf($event), 1)
      "
      @addDashboardName="userDashboards.push($event)"
      v-if="reportingInterface === 'dashboardMaker'"
      @reportingInterface="reportingInterface = $event"
      :selectedDashboard="selectedDashboard"
    />

    <schema-options
      @addCubeName="userCubesNames.push($event)"
      v-if="reportingInterface === 'addCube'"
    >
    </schema-options>
    <!-- <keep-alive> -->
    <query-builder
      @removePivotTableName="
        userPivotTables.splice(userPivotTables.indexOf($event), 1)
      "
      @addPivotTableName="userPivotTables.push($event)"
      :selectedPivotTable="selectedPivotTable"
      v-if="reportingInterface === 'QBuilder'"
    ></query-builder>
    <!-- </keep-alive> -->

    <notifications group="user" position="top center" />
  </div>
</template>

<script>
import axios from "axios";
import Cubes from "./components/cubes/the-cubes-names.vue";
import UserDashboards from "./components/reporting/userDashboards";
import DashboardMaker from "./components/reporting/dashboardMaker";
import QueryBuilder from "./components/reporting/queryBuilder";
import SchemaOptions from "./components/cubes/base-add-cube";
import UserPivotTables from "./components/reporting/userPivotTables";

export default {
  data: function() {
    return {
      reportingInterface: "main",
      selectedDashboard: null,
      selectedPivotTable: null,
      userPivotTables: [],
      userDashboards: [],
      userCubesNames: [],
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

  mounted() {
    this.getAllPivotTables();
    this.getAllDashboards();
    this.getCubes();
  },

  methods: {
    getAllPivotTables() {
      const pivotTables = [];
      axios
        .get("/api/pivottable/all")
        .then(response => {
          return response.data;
        })
        .then(data => {
          for (let key in data) {
            pivotTables.push(data[key]);
          }
        });
      this.userPivotTables = pivotTables;
    },

    getAllDashboards() {
      const Dashboards = [];
      axios
        .get("/api/dashboard/all")
        .then(response => {
          return response.data;
        })
        .then(data => {
          for (let key in data) {
            Dashboards.push(data[key]);
          }
        });
      this.userDashboards = Dashboards;
    },

    getCubes: function() {
      const cubes = [];
      axios
        .get("/api/cubes")
        .then(response => {
          return response.data;
        })
        .then(data => {
          for (let key in data) {
            cubes.push(data[key]);
          }
        });
      this.userCubesNames = cubes;
    },
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
