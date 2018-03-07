<template>
  <div>
    <input type="button" value="new dashboard" @click="selectCubeModal = true"/>

    <select-cube-dashboard v-show="selectCubeModal"/>
  </div>
</template>


<script>

  import selectCubeDashboard from './selectCubeDashboard'

  export default {
    data: function () {
      return {
        selectCubeModal: false
      };
    },
    components: {
      'select-cube-dashboard': selectCubeDashboard
    }
  };

</script>

<style>

</style>
