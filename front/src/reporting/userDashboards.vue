<template>
  <div>
    my dashboard :
    <div style="float: bottom" v-for="dashboard in userDashboards">
      <input type="button" :value="dashboard">
      <button class="btn btn-primary btn-xs" data-title="Edit"><span
        class="glyphicon glyphicon-pencil"></span></button>
      <button class="btn btn-danger btn-xs" data-title="Delete"><span
        class="glyphicon glyphicon-trash"></span></button>
    </div>
  </div>

</template>

<script>
  export default {

    data: function () {
      return {
        userDashboards: [],
      };
    },
    created() {
      this.$http
        .get("dash_api/dashboards")
        .then(response => {
          return response.json();
        })
        .then(data => {
          for (let key in data) {
            this.userDashboards.push(data[key]);
          }
        });
    },
  }
</script>

<style scoped>

</style>
