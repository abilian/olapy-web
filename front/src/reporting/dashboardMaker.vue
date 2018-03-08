<template>
  <div>
    my dashboard :

    <div class="dash-toolbox">
      <!--todo change flask or vue delimiter-->
      <img class="toolbox-icons"
           src="https://cdn4.iconfinder.com/data/icons/flat-business-icon-set/450/bar_chart-512.png"/>
      <img class="toolbox-icons"
           src="http://www.myiconfinder.com/uploads/iconsets/256-256-08f7586f151e4761d26cb03276ac9b71.png"/>

    </div>
  </div>

</template>

<script>
  export default {
    data: function () {
      return {};
    },
    created() {
    },
  };
</script>

<style scoped>

  .dash-toolbox {
    position: fixed;
    margin: 36% 22%;
    background: #c7ddef;
    width: 50%;
    height: 50px;
    border-radius: 25px;
    float: right;
  }

  .toolbox-icons {
  margin: 10px 0 0 15px;
  width: 30px;
  height: 30px;
  }

</style>
