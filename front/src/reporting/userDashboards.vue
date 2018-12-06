<template>
  <li id="dashboard-section">
    <div class="nav-btn">
      <button class="white-btn" @click="$emit('reportingInterface', 'main');">
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
      <li v-for="dashboard in userDashboards">
        <button
          class="btn btn-default btn-outline btn-rounded m-b-10"
          @click="selectDashboard(dashboard);"
        >
          {{ dashboard }}
        </button>
      </li>
    </ul>
  </li>
</template>

<script>
const axios = require("axios");
export default {
  props: {
    refreshDashboards: Boolean,
  },
  data: function() {
    return {
      userDashboards: [],
    };
  },
  methods: {
    selectDashboard(dashboard) {
      axios.get("api/dashboard/" + dashboard).then(response => {
        this.$emit("selectedDashboard", response.body);
        this.$emit("reportingInterface", "dashboardMaker");
      });
    },
    getAllDashboards() {
      let Dashboards = [];
      axios
        .get("api/dashboard/all")
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
  },

  watch: {
    refreshDashboards: function(val) {
      if (val === true) {
        this.getAllDashboards();
        this.$emit("refreshDashboards", false);
      }
    },
  },
  mounted() {
    this.getAllDashboards();
  },
};
</script>

<style scoped></style>
