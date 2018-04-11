<template>
  <div>
    <!--<form @submit="saveDashboard" action="#" method="post">-->
    <label>
      Dashboard name:
      <input type="text" v-model="dashboardName" required>
    </label>

    <input style="float: right;" type="submit" value="save" @click="saveDashboard">
    {{layout}}
    *********************
    {{usedCharts}}
    ---------------------------
    {{selectedDashboard}}
    <chart-props :currentChartDiv="currentChartDiv" :chartType="draggedChart" v-if="showChartProps === true"
                 @showChartProps="showChartProps = $event"></chart-props>
    <draggable id="divDash" v-model="usedCharts" class="dashboard" :options="{group:'charts', sort: false}">

      <div v-for="(element, index) in usedCharts" :id="element.type + (index)">{{element.type + (index)}}</div>

      <grid-layout
        :layout="layout"
        :col-num="12"
        :row-height="30"
        :is-draggable="true"
        :is-resizable="true"
        :is-mirrored="false"
        :vertical-compact="true"
        :margin="[10, 10]"
        :use-css-transforms="true">

        <grid-item v-for="(item, index) in layout" v-show="index < layout.length - 1"
                   :x="item.x"
                   :y="item.y"
                   :w="item.w"
                   :h="item.h"
                   :i="item.i"
                   @resize="resize">
          <button type="button" class="btn btn-danger btn-lg" style="margin-right: 0; float: right"
                  @click="removeItem(item.i)"><span
            class="glyphicon glyphicon-remove"></span></button>
        </grid-item>
      </grid-layout>
    </draggable>
    <draggable :list="chartTypes" class="dash-toolbox" :move="onMove"
               :options="{group:{ name:'charts',  pull:'clone' }}">
      <div v-for="chart_type in chartTypes">
        <img class="toolbox-icons" :src="'/static/icons/' + chart_type + 'chart.png'">
      </div>
    </draggable>

    <!--</form>-->
  </div>

</template>

<script>
import Plotly from "plotly.js";
import draggable from "vuedraggable";
import VueGridLayout from "vue-grid-layout";
import ChartProps from "./chartProps";

let GridLayout = VueGridLayout.GridLayout;
let GridItem = VueGridLayout.GridItem;

export default {
  props: ["selectedDashboard"],
  data: function() {
    return {
      layout : [{x: 0, y: 0, w: 6, h: 8, i: "0"}],
      usedCharts : [],
      dashboardName : "",
      showChartProps: false,
      currentChartDiv: "",
      chartTypes: ["bar", "scatter", "pie"],
      draggedChart: "",
    };
  },
  methods: {
    removeItem(index) {
      let i = this.layout.map(item => item.i).indexOf(index);
      this.usedCharts.splice(i, 1);
      this.layout.splice(i, 1);
    },
    onMove({relatedContext, draggedContext}) {
      this.draggedChart = draggedContext.element;
      // this.draggedChart = this.list[draggedContext.index];
    },
    resize: function (id) {
      let plotDiv = document.getElementById(id);
      Plotly.Plots.resize(plotDiv);
    },
    saveDashboard() {
      // let dashboardContent = document.getElementById('divDash').querySelectorAll('*')
      if (this.dashboardName) {
        let data = {
          dashboardName: this.dashboardName,
          usedCharts: this.usedCharts,
          layout : this.layout
          // dashboardContent: stringify(document.getElementById('divDash').children)
        };
        this.$http.post("api/dashboard/save", data)
      }
    },
  },
  components: {
    draggable,
    GridLayout,
    GridItem,
    "chart-props": ChartProps,
  },
  watch: {
    usedCharts: function(list, oldList) {
      if (list.length > oldList.length) {
        // watch when add only/ not when remove
        let chartDiv = this.draggedChart + (list.length - 1);
        this.layout[list.length - 1].i = chartDiv;
        this.layout.push({ x: 0, y: 0, w: 6, h: 8, i: "" }); //prepare next div //todo calculation
        //create div dynamically
        let gridItems = document.getElementsByClassName("vue-grid-item");
        let divDash = gridItems[gridItems.length - 2]; //-2 because last element is the vue-grid-placeholder
        let innerDiv = document.createElement("div");
        innerDiv.id = chartDiv;
        this.currentChartDiv = chartDiv;
        divDash.appendChild(innerDiv);
        this.showChartProps = true;
      }
    },
  },
  created() {
    if (this.selectedDashboard) {
      this.layout = this.selectedDashboard['charts_layout'];
      this.usedCharts = this.selectedDashboard['charts'];
      this.dashboardName = this.selectedDashboard['name']
    }
  },
};
</script>

<style scoped>
.dash-toolbox {
  position: fixed;
  margin: 32% 22%;
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

.vue-grid-item:not(.vue-grid-placeholder) {
  background: #ccc;
  border: 1px solid black;
}

.vue-grid-item.resizing {
  opacity: 0.9;
}

.vue-grid-item.static {
  background: #cce;
}

.vue-grid-item .text {
  font-size: 24px;
  text-align: center;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  height: 100%;
  width: 100%;
}

.vue-grid-item .no-drag {
  height: 100%;
  width: 100%;
}

.vue-grid-item .minMax {
  font-size: 12px;
}

.vue-grid-item .add {
  cursor: pointer;
}

.btn-lg {
  padding: 10px 13px;
}
</style>
