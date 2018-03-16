<template>
  <div>
    my dashboard :

    <draggable id="divDash" v-model="list2" class="dashboard" :options="{group:'charts', sort: false}">
      {{layout}}
        <!--<div v-for="(element, index) in list2" :id="element.type + (index)">{{element.type + (index)}}</div>-->
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


    <draggable v-model="list" class="dash-toolbox" :move="onMove"
               :options="{group:{ name:'charts',  pull:'clone' }}">
      <div><img :key="0" class="toolbox-icons"
                src="https://cdn4.iconfinder.com/data/icons/flat-business-icon-set/450/bar_chart-512.png"/></div>
      <div><img :key="2" class="toolbox-icons"
                src="http://www.myiconfinder.com/uploads/iconsets/256-256-08f7586f151e4761d26cb03276ac9b71.png"/>
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
import Plotly from "plotly.js";
import draggable from "vuedraggable";
import VueGridLayout from "vue-grid-layout";

var GridLayout = VueGridLayout.GridLayout;
var GridItem = VueGridLayout.GridItem;

export default {
  data: function() {
    return {
      layout: [{ x: 0, y: 0, w: 6, h: 8, i: "0"}],
      list: [
        {
          type: "bar",
        },
        {
          type: "scatter",
        },
        {
          type: "pie",
        },
      ],

      list2: [],
      draggedChart: "",
    };
  },
  methods: {
    removeItem(index) {
      let i = this.layout.map(item => item.i).indexOf(index);
      this.list2.splice(i, 1);
      this.layout.splice(i, 1);
    },
    genGraph(grapheType) {
      if (grapheType === "bar") {
        //todo replace with rest api
        let data = [
          {
            x: ["giraffes", "orangutans", "monkeys"],
            y: [20, 14, 23],
            type: "bar",
          },
        ];
        return {
          data: data,
        };
      } else if (grapheType === "pie") {
        let data = [
          {
            values: [19, 26, 55],
            labels: ["Residential", "Non-Residential", "Utility"],
            type: "pie",
          },
        ];

        // let layout = {
        //   height: 400,
        //   width: 500,
        // };
        return {
          data: data,
          // layout: layout,
        };
      }
    },
    onMove({ relatedContext, draggedContext }) {
      this.draggedChart = draggedContext.element.type;
    },
    resize: function (i, newH, newW) {
      let plotDiv = document.getElementById(i);
      Plotly.Plots.resize(plotDiv);
    }
  },

  components: {
    draggable,
    GridLayout,
    GridItem,
  },
  watch: {
    list2: function (list, oldList) {
      if (list.length > oldList.length) { // watch when add only/ not when remove
        let chartDiv = this.draggedChart + (list.length - 1);
        this.layout[list.length - 1].i = chartDiv;
        this.layout.push({x: 0, y: 0, w: 6, h: 8, i: ""}); //prepare next div //todo calculation
        //create div dynamically
        let gridItems = document.getElementsByClassName("vue-grid-item");
        let divDash = gridItems[gridItems.length - 2]; //-2 because last element is the vue-grid-placeholder
        let innerDiv = document.createElement("div");
        innerDiv.id = chartDiv;
        divDash.appendChild(innerDiv);
        let graph = this.genGraph(this.draggedChart);
        Plotly.newPlot(chartDiv, graph.data, graph.layout)
          .then(function () {
            let graphDiv = document.getElementById(chartDiv);
            graphDiv.style.width = "95%";
            graphDiv.style.height = "95%";
            return Plotly.Plots.resize(graphDiv);
          });
      }

    },
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

  /*** EXAMPLE ***/
#content {
    width: 100%;
}

.vue-grid-layout {
    background: #eee;
}

.layoutJSON {
    background: #ddd;
    border: 1px solid black;
    margin-top: 10px;
    padding: 10px;
}

.eventsJSON {
    background: #ddd;
    border: 1px solid black;
    margin-top: 10px;
    padding: 10px;
    height: 100px;
    overflow-y: scroll;
}

.columns {
    -moz-columns: 120px;
    -webkit-columns: 120px;
    columns: 120px;
}



.vue-resizable-handle {
    z-index: 5000;
    position: absolute;
    width: 20px;
    height: 20px;
    bottom: 0;
    right: 0;
    background: url('data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/Pg08IS0tIEdlbmVyYXRvcjogQWRvYmUgRmlyZXdvcmtzIENTNiwgRXhwb3J0IFNWRyBFeHRlbnNpb24gYnkgQWFyb24gQmVhbGwgKGh0dHA6Ly9maXJld29ya3MuYWJlYWxsLmNvbSkgLiBWZXJzaW9uOiAwLjYuMSAgLS0+DTwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+DTxzdmcgaWQ9IlVudGl0bGVkLVBhZ2UlMjAxIiB2aWV3Qm94PSIwIDAgNiA2IiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjojZmZmZmZmMDAiIHZlcnNpb249IjEuMSINCXhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiDQl4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjZweCIgaGVpZ2h0PSI2cHgiDT4NCTxnIG9wYWNpdHk9IjAuMzAyIj4NCQk8cGF0aCBkPSJNIDYgNiBMIDAgNiBMIDAgNC4yIEwgNCA0LjIgTCA0LjIgNC4yIEwgNC4yIDAgTCA2IDAgTCA2IDYgTCA2IDYgWiIgZmlsbD0iIzAwMDAwMCIvPg0JPC9nPg08L3N2Zz4=');
    background-position: bottom right;
    padding: 0 3px 3px 0;
    background-repeat: no-repeat;
    background-origin: content-box;
    box-sizing: border-box;
    cursor: se-resize;
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

.vue-draggable-handle {
    position: absolute;
    width: 20px;
    height: 20px;
    top: 0;
    left: 0;
    background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><circle cx='5' cy='5' r='5' fill='#999999'/></svg>") no-repeat;
    background-position: bottom right;
    padding: 0 8px 8px 0;
    background-repeat: no-repeat;
    background-origin: content-box;
    box-sizing: border-box;
    cursor: pointer;
}

.btn-lg {
  padding: 10px 13px;
}
</style>
