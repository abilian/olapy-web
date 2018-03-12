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
        <!--<div class="table-responsive" v-html="resultCube">-->
      </draggable>
      <h2>List 2 Draggable</h2>
      <draggable v-model="list2" class="dashboard" :options="{group:'charts'}">
        <!--style="border-style: dotted; background-color: white; border-color: #c7ddef"-->
        <div  v-for="(element, index) in list2" :id="element.type + (index - 1)">{{element.type + (index - 1)}}</div>
        <!--<div id="pie"></div>-->
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
          type: "pie"
        }, {
          type: "scatter"
        }, {
          type: "bar"
        }],


        list2: [{
          type: "-"
        }]
      };
    },
    methods: {
      genGraph(grapheType) {
        if (grapheType === 'bar') {
          //todo replace with rest api
          let data = [{
            x: ['giraffes', 'orangutans', 'monkeys'],
            y: [20, 14, 23],
            type: 'bar'
          }];
          return {
            'data': data
          }
        }
        else if (grapheType === 'pie') {
          let data = [{
            values: [19, 26, 55],
            labels: ['Residential', 'Non-Residential', 'Utility'],
            type: 'pie'
          }];

          let layout = {
            height: 400,
            width: 500
          };
          return {
            'data': data,
            'layout': layout
          }
        }


      }
    },
    components: {
      draggable,
    },
    watch: {

      list2: function (list) {
        let chartType = list[[list.length - 1]].type;
        console.log(chartType);
        let chartDiv = chartType + (list.length - 3); // - 2 normalement
        let graph = this.genGraph(chartType);
        Plotly.newPlot(chartDiv, graph.data, graph.layout);

      }
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
