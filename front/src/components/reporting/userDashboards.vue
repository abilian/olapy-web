<template>
  <li id="dashboard-section">
    <div class="nav-btn">
      <button class="white-btn" @click="$emit('reportingInterface', 'main')">
        <i class="fa fa-tachometer"></i> <span>Dashboards</span>
      </button>
    </div>
    <a class="has-arrow  " href="#" aria-expanded="false">
      <span class="hide-menu">
        <span class="label label-rouded label-primary pull-right">{{
          userDashboards.length
        }}</span>
      </span>
    </a>
    <ul aria-expanded="false" class="collapse">
      <li v-for="(dashboard, index) in userDashboards" :key="dashboard + index">
        <button
          class="btn btn-default btn-outline btn-rounded m-b-10"
          @click="selectDashboard(dashboard)"
        >
          {{ dashboard }}
        </button>
      </li>
    </ul>
  </li>
</template>

<script>
import axios from "axios";

export default {
  props: {
    userDashboards: Array,
  },

  methods: {
    selectDashboard(dashboard) {
      this.$emit("reportingInterface", "");
      axios.get("/api/dashboard/" + dashboard).then(response => {
        this.$emit("selectedDashboard", response.data);
        this.$emit("reportingInterface", "dashboardMaker");
      });
    },
  },
};
</script>
