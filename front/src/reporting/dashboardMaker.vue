<template>
  <div>
    <!--<form @submit="saveDashboard" action="#" method="post">-->
    <label>
      Dashboard name:
      <input type="text" v-model="dashboardName" required>
    </label>

    <input style="float: right;" type="submit" value="save" @click="saveDashboard">
    <input style="float: right;" type="button" :value=" 'enable modification :' + allowModification"
           @click="allowModification = !allowModification">
    <chart-props
      :currentChartDiv="currentChartDiv"
      :chartType="draggedChart"
      v-if="showChartProps === true"
      @chartData="chartData.push($event)"
      @selectedCube="selectedCube =$event"
      @showChartProps="showChartProps = $event"/>


    <draggable
      id="divDash"
      v-model="usedCharts"
      class="dashboard"
      :options="{group:'charts', sort: false}">

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

            <button type="button"
                    class="btn btn-danger btn-lg"
                    style="margin-right: 0; float: right"
                    @click="removeItem(item.i)">
              <span class="glyphicon glyphicon-remove"></span></button>
          </grid-item>

      </grid-layout>

    </draggable>

    <draggable
      :list="chartTypes"
      class="dash-toolbox"
      :move="onMove"
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
  props: {
    selectedDashboard: String,
  },
  data: function() {
    return {
      allowModification: true,
      layout: [{ x: 0, y: 0, w: 6, h: 8, i: "0" }],
      usedCharts: [],
      dashboardName: "",
      showChartProps: false,
      currentChartDiv: "",
      chartTypes: ["bar", "scatter", "pie"],
      draggedChart: "",
      chartData: [],
    };
  },
  methods: {
    removeItem(index) {
      let i = this.layout.map(item => item.i).indexOf(index);
      this.usedCharts.splice(i, 1);
      this.layout.splice(i, 1);
    },
    onMove({ relatedContext, draggedContext }) {
      this.draggedChart = draggedContext.element;
      // this.draggedChart = this.list[draggedContext.index];
    },
    resize: function(id) {
      let plotDiv = document.getElementById(id);
      Plotly.Plots.resize(plotDiv);
    },
    saveDashboard() {
      // let dashboardContent = document.getElementById('divDash').querySelectorAll('*')
      if (this.dashboardName) {
        let data = {
          dashboardName: this.dashboardName,
          usedCharts: this.usedCharts,
          layout: this.layout,
          chartData: this.chartData,
          // dashboardContent: stringify(document.getElementById('divDash').children)
        };
        this.$http.post("api/dashboard/save", data);
      } else {
        alert("missing dashboardName");
      }
    },
  },
  components: {
    draggable,
    GridLayout,
    GridItem,
    chartProps: ChartProps,
  },
  watch: {
    usedCharts: function(list, oldList) {
      if (list.length > oldList.length && this.allowModification) {
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
      this.allowModification = false;
      this.layout = this.selectedDashboard["charts_layout"];
      this.usedCharts = this.selectedDashboard["used_charts"];
      this.dashboardName = this.selectedDashboard["name"];
      this.chartData = this.selectedDashboard["charts_data"];
    }
  },
  mounted: function() {
    if (this.selectedDashboard) {
      let gridItems = document.getElementsByClassName("vue-grid-item");
      for (let chart_data in this.selectedDashboard["charts_data"]) {
        let divDash = gridItems[chart_data];
        let innerDiv = document.createElement("div");
        innerDiv.id = this.layout[chart_data].i;
        divDash.appendChild(innerDiv);
        Plotly.newPlot(
          this.layout[chart_data].i,
          this.selectedDashboard["charts_data"][chart_data].data,
          this.selectedDashboard["charts_data"][chart_data].layout
        );
        let graphDiv = document.getElementById(this.layout[chart_data].i);
        graphDiv.style.width = "95%";
        graphDiv.style.height = "95%";
        Plotly.Plots.resize(graphDiv);
      }
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
