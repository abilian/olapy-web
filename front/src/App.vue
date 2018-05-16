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

              <li>
                  <a href="#" aria-expanded="false"><i class="fa fa-columns"></i>
                      <span @click="runQueryBuilder()">Query Builder</span></a>
              </li>

          </ul>
        </nav>
        <!-- End Sidebar navigation -->
      </div>
      <!-- End Sidebar scroll-->

    </div>

      <div class="page-wrapper" v-if="reportingInterface==='main'">
          <div class="row page-titles">
              <div class="col-md-5 align-self-center">
                  <button type="button" class="btn btn-primary btn-flat btn-addon m-b-10 m-l-5"
                          @click="reportingInterface='dashboardMaker'"><i class="ti-plus"></i>New Dashboard
                  </button>
              </div>
          </div>
      </div>

      <dashboard-maker v-if="reportingInterface==='dashboardMaker' "
                       :selectedDashboard="selectedDashboard"/>


      <schema-options v-if="reportingInterface==='addCube' "></schema-options>

      <query-builder :DataFrameCsv="DataFrameCsv" v-if="reportingInterface==='QBuilder' "></query-builder>

  </div>


</template>


<script>
import Cubes from "./cubes/the-cubes-names.vue";
import UserDashboards from "./reporting/userDashboards";
import DashboardMaker from "./reporting/dashboardMaker";
import QueryBuilder from "./reporting/queryBuilder";
import SchemaOptions from "./cubes/base-schema-options";

export default {
  data: function() {
    return {
      reportingInterface: "main",
      selectedDashboard: "",
      DataFrameCsv: null,
    };
  },
  methods: {
    runQueryBuilder() {
      this.$http
        .get("api/query_builder")
        .then(response => {
          return response.json();
        })
        .then(data => {
          //when i put this in queryBuilder.vue it didn't work
          this.DataFrameCsv = data;
          this.reportingInterface = "QBuilder";
        });
    },
  },
  components: {
    userCubes: Cubes,
    schemaOptions: SchemaOptions,
    userDashboards: UserDashboards,
    dashboardMaker: DashboardMaker,
    queryBuilder: QueryBuilder,
  },
};
</script>

<style>
</style>
