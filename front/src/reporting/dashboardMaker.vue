<template>
  <div>
    my dashboard :


      <draggable v-model="list" class="dash-toolbox" :options="{group:{ name:'charts',  pull:'clone', put:false }}">
        <div><img class="toolbox-icons"
                  src="https://cdn4.iconfinder.com/data/icons/flat-business-icon-set/450/bar_chart-512.png"/></div>
        <div><img class="toolbox-icons"
                  src="http://www.myiconfinder.com/uploads/iconsets/256-256-08f7586f151e4761d26cb03276ac9b71.png"/>
        </div>
        <!--<h4 class="title">Pie</h4>-->
        <!--<div ref="pie"></div>-->
        <!--<div v-for="(element, index) in list" :key="index">{{element.name}}</div>-->
      </draggable>
      <h2>List 2 Draggable</h2>
      <draggable v-model="list2" class="dashboard" :options="{group:'charts'}">
        <div v-for="(element, index) in list2" :key="index">{{element.name}}</div>
      </draggable>



    <!--<div class="dash-toolbox">-->
      <!--&lt;!&ndash;todo change flask or vue delimiter&ndash;&gt;-->
      <!--<img class="toolbox-icons"-->
           <!--src="https://cdn4.iconfinder.com/data/icons/flat-business-icon-set/450/bar_chart-512.png"/>-->
      <!--<img class="toolbox-icons"-->
           <!--src="http://www.myiconfinder.com/uploads/iconsets/256-256-08f7586f151e4761d26cb03276ac9b71.png"/>-->

    <!--</div>-->
  </div>

</template>

<script>

  import Plotly from 'plotly.js'
  import draggable from 'vuedraggable'

  export default {
    data: function () {
      return {
        list: [{
          name: "Pie"
        }, {
          name: "Bar"
        }, {
          name: "Scatter"
        }],
        list2: [{
          name: "fig1"
        }, {
          name: "fig2"
        }, {
          name: "fig3"
        }]
      };
    },
    methods: {
      // add: function () {
      //   this.list.push({
      //     name: 'Bar'
      //   });
      // },
      // replace: function () {
      //   this.list = [{
      //     name: 'Pie'
      //   }]
      // }
    },
    components: {
      draggable,
    },
    mounted () {
      // Plotly.plot(
      //   this.$refs.pie,
      //   [{
      //     values: [19, 26, 55],
      //     labels: ['Residential', 'Non-Residential', 'Utility'],
      //     type: 'pie'
      //   }],
      //   {
      //     margin: {t: 0, l: 0, b: 0, r: 0}
      //   }
      // )
    }
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
    float: left;
  }


  .dashboard {
    height: 50%;
    width: 100%;
  }
</style>
