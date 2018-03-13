<template>
  <div>
    my dashboard :
    <draggable v-model="list" class="dash-toolbox" :move="onMove"
               :options="{group:{ name:'charts',  pull:'clone' }}">
      <div><img class="toolbox-icons"
                src="https://cdn4.iconfinder.com/data/icons/flat-business-icon-set/450/bar_chart-512.png"/></div>
      <div><img class="toolbox-icons"
                src="http://www.myiconfinder.com/uploads/iconsets/256-256-08f7586f151e4761d26cb03276ac9b71.png"/>
      </div>

    </draggable>


    <draggable v-model="list2" class="dashboard" :options="{group:'charts'}">
      <!--style="border-style: dotted; background-color: white; border-color: #c7ddef"-->
      <div id="divDash">
        <!--<div v-for="(element, index) in list2" :id="element.type + (index)">{{element.type + (index)}}</div>-->
      </div>
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


        list2: [],
        draggedChart : ''
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


      },
      onMove({relatedContext, draggedContext}) {
        this.draggedChart = draggedContext.element.type;

      }
    },

    components: {
      draggable,
    },
    watch: {

      list2: function (list) {
        // let chartType = list[[list.length - 1]].type;
        let chartDiv = this.draggedChart + (list.length - 2);
        // let chartDiv = chartType + (list.length - 2);

        //create div dynamically
        let divDash = document.getElementById('divDash');
        let innerDiv = document.createElement('div');
        innerDiv.id = chartDiv;
        divDash.appendChild(innerDiv);

        let graph = this.genGraph(this.draggedChart);
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
    border-style: dotted;
    height: 50px;
    width: 100%;
  }
</style>
