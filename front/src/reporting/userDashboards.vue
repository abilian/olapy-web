<template>
    <li id="dashboard-section">
        <a class="has-arrow  " href="#" aria-expanded="false">
            <i class="fa fa-tachometer"></i>
            <span @click="$emit('reportingInterface', 'main')" class="hide-menu">Dashboards
                    <span class="label label-rouded label-primary pull-right">{{userDashboards.length}}</span>
                  </span>
        </a>
        <ul aria-expanded="false" class="collapse">
            <li v-for="dashboard in userDashboards">
                <button class="btn btn-default btn-outline btn-rounded m-b-10"
                        @click="selectDashboard(dashboard)">{{dashboard}}
                </button>
            </li>
        </ul>
    </li>

</template>

<script>
export default {
  data: function() {
    return {
      userDashboards: [],
    };
  },
  methods: {
    selectDashboard(dashboard) {
      this.$http.get("api/dashboard/" + dashboard).then(response => {
        this.$emit("selectedDashboard", response.body);
        this.$emit("reportingInterface", "dashboardMaker");
      });
    },
  },
  created() {
    this.$http
      .get("api/dashboard/all")
      .then(response => {
        return response.json();
      })
      .then(data => {
        for (let key in data) {
          this.userDashboards.push(data[key]);
        }
      });
  },
};
</script>

<style scoped>
</style>
