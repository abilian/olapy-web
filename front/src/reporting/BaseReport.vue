<template>
  <div>


    <ul id="example-1">
      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
      <li v-for="item in items">
        {{ item.message }}
        << item.message >>
      </li>
    </ul>

    <div v-if="reportingInterface !== 'dashboardMaker'">
      {% block  page_header %}
      <input type="button" value="new dashboard" @click="reportingInterface = 'dashboardMaker'"/>
      <!--<select-cube-dashboard v-if="reportingInterface === 'newDashboard'"-->
      <!--@selectedCube="selectedCube = $event" @interface="reportingInterface = $event"/>-->
      <!--<hr>-->

      {% endblock %}
      <user-dashboards
        @selectedDashboard="selectedDashboard = $event"
       @reportingInterface="reportingInterface = $event"/>

    </div>

    <dashboard-marker
      v-if="reportingInterface === 'dashboardMaker'"
      :selectedDashboard="selectedDashboard"
      @interface="reportingInterface = $event"/>

  </div>

</template>


<script>
import selectCubeDashboard from "./selectCubeDashboard";
import userDashboards from "./userDashboards";
import dashboardMarker from "./dashboardMaker";

export default {
  delimiters: ["<<", ">>"],
  data: function() {
    return {
      reportingInterface: "main",
      items: [
          {message: 'Foo'},
          {message: 'Bar'}
      ]
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
